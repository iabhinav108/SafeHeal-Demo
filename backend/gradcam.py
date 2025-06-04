import torch
import torch.nn as nn
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
import os
import timm

class GradCAM:
    def __init__(self, model, target_layer, device):
        
        self.model = model.to(device)
        self.target_layer = target_layer
        self.device = device
        
        self.model.eval()
        
        self.gradients = None
        self.activations = None
        
        self.forward_hook = self.target_layer.register_forward_hook(self.save_activation)
        self.backward_hook = self.target_layer.register_full_backward_hook(self.save_gradient)
    
    def save_activation(self, module, input, output):
        self.activations = output.detach()
    
    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate_cam(self, input_tensor, target_class=None):
        
        output = self.model(input_tensor)
        
        if target_class is None:
            target_class = torch.argmax(output)
            
        target_idx = target_class.item() if isinstance(target_class, torch.Tensor) else target_class
        print(f"Generating GradCAM for class index: {target_idx}")
        
        self.model.zero_grad()
        output[0, target_class].backward()
        
        if self.gradients is None:
            print("Warning: No gradients computed. Check if the target layer is correctly specified.")
            return np.zeros((1, 1))
        
        weights = torch.mean(self.gradients, dim=[0, 2, 3])
        
        cam = torch.zeros_like(self.activations[0, 0]).detach()
        for i, w in enumerate(weights):
            cam += w * self.activations[0, i]
        
        cam = cam.cpu().numpy()
        cam = np.maximum(cam, 0)
        
        if np.max(cam) > 0:
            cam = cam / np.max(cam)
        
        return cam
    
    def overlay_cam_on_image(self, img, cam, alpha=0.5):
        
        cam = cv2.resize(cam, (img.shape[1], img.shape[0]))
        
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        visualization = heatmap * alpha + img * (1 - alpha)
        visualization = visualization / np.max(visualization)
        
        return np.uint8(255 * visualization)
    
    def close(self):
        self.forward_hook.remove()
        self.backward_hook.remove()


def load_parallel_model(model_path, model_class, device, strict=True, **model_kwargs):
    abs_model_path = os.path.abspath(model_path)
    print(f"Loading model from: {abs_model_path}")
    
    if not os.path.exists(abs_model_path):
        raise FileNotFoundError(f"Model file not found: {abs_model_path}")
    
    try:
        model = model_class(**model_kwargs).to(device)
    except Exception as e:
        print(f"Error initializing model: {e}")
        raise
    
    try:
        state_dict = torch.load(abs_model_path, map_location=device)
    except Exception as e:
        print(f"Error loading model file: {e}")
        raise
    
    if isinstance(state_dict, dict) and 'state_dict' in state_dict:
        state_dict = state_dict['state_dict']
    
    if any(k.startswith('module.') for k in state_dict.keys()):
        from collections import OrderedDict
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:] if k.startswith('module.') else k 
            new_state_dict[name] = v
        state_dict = new_state_dict
    
    try:
        model.load_state_dict(state_dict, strict=strict)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error during state_dict loading: {e}")
        if not strict:
            print("Continuing with non-strict loading")
        else:
            raise
    
    return model


def visualize_classification_gradcam(image_path, model, target_layer, preprocess, class_names, device='cuda', output_dir=None):
    
    img = Image.open(image_path).convert('RGB')
    input_tensor = preprocess(img).unsqueeze(0).to(device)
    
    orig_img = np.array(img)
    
    grad_cam = GradCAM(model, target_layer, device)
    
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        
        top_probs, top_indices = torch.topk(probabilities, 3)
        top_probs = top_probs.squeeze().cpu().numpy()
        top_indices = top_indices.squeeze().cpu().numpy()
    
    predicted_class = top_indices[0]
    cam = grad_cam.generate_cam(input_tensor, predicted_class)
    
    visualization = grad_cam.overlay_cam_on_image(orig_img, cam)
    
    grad_cam.close()
    
    plt.figure(figsize=(8, 8))
    
    plt.subplot(1, 2, 1)
    plt.imshow(orig_img)
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(visualization)
    class_name = class_names[predicted_class] if predicted_class < len(class_names) else f'Class {predicted_class}'
    plt.title(f'GradCAM: {class_name}\nConfidence: {top_probs[0]:.2%}')
    plt.axis('off')
    
    plt.figtext(0.5, 0.01, f"Top predictions:", ha='center', fontsize=12, fontweight='bold')
    
    for i, (idx, prob) in enumerate(zip(top_indices, top_probs)):
        class_name = class_names[idx] if idx < len(class_names) else f'Class {idx}'
        plt.figtext(0.5, -0.05 - i*0.025, f"{i+1}. {class_name}: {prob:.2%}", ha='center', fontsize=11)
    
    plt.tight_layout()
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.basename(image_path).split('.')[0]
        plt.savefig(os.path.join(output_dir, f"gradcam_{base_name}.png"), bbox_inches='tight')
    
    plt.show()


class CustomEdgeNeXt(nn.Module):
    def __init__(self, num_classes=10, dropout_rate=0.3):
        super(CustomEdgeNeXt, self).__init__()
        base_model = timm.create_model("edgenext_small", pretrained=True, num_classes=0, global_pool='')
        self.feature_extractor = base_model
        
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.flatten = nn.Flatten()
        self.classifier = nn.Sequential(
            nn.Linear(base_model.num_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(512, num_classes)
        )
    def forward(self, x):
        x = self.feature_extractor(x)   
        x = self.pool(x) 
        x = self.flatten(x) 
        x = self.classifier(x)   
        return x


def find_target_layer_for_edgenext(model):
    if hasattr(model.feature_extractor, 'stages') and len(model.feature_extractor.stages) > 0:
        last_stage = model.feature_extractor.stages[-1]
        
        if hasattr(last_stage, 'blocks') and len(last_stage.blocks) > 0:
            last_block = last_stage.blocks[-1]
            for name, module in reversed(list(last_block.named_modules())):
                if isinstance(module, nn.Conv2d):
                    print(f"Found target layer in last stage block: {name}")
                    return module
        
        for name, module in reversed(list(last_stage.named_modules())):
            if isinstance(module, nn.Conv2d):
                print(f"Found target layer in last stage: {name}")
                return module
    
    for name, module in reversed(list(model.feature_extractor.named_modules())):
        if isinstance(module, nn.Conv2d):
            print(f"Found target layer in feature extractor: {name}")
            return module
    
    print("Warning: Could not find a suitable convolutional layer. Using entire feature extractor.")
    return model.feature_extractor


if __name__ == "__main__":
    class_names = ['Abrasions', 'Bruises', 'Burns', 'Cut', 'Diabetic Wounds', 
                   'Laseration', 'Normal', 'Pressure Wounds', 'Surgical Wounds', 'Venous Wounds']
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.abspath(os.path.join(script_dir, "../models/edgenext_wound_classifier_weights.pth"))
    
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for model at: {model_path}")
    
    image_path = os.path.join(script_dir, "../data/test_images/classification/burns (33).jpg")
    
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    
    try:
        model = load_parallel_model(
            model_path, 
            CustomEdgeNeXt, 
            device, 
            strict=False,
            num_classes=len(class_names),
            dropout_rate=0.3
        )
        
        target_layer = find_target_layer_for_edgenext(model)
        
        visualize_classification_gradcam(
            image_path, 
            model, 
            target_layer, 
            preprocess, 
            class_names, 
            device=device,
            output_dir="gradcam_results"
        )
        
    except Exception as e:
        print(f"Error running GradCAM: {e}")
        import traceback
        traceback.print_exc()