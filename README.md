# SafeHeal: AI-Powered Wound Segmentation and Classification

SafeHeal is an innovative application that leverages computer vision and artificial intelligence to analyze wound images, providing healthcare professionals with valuable insights for wound assessment and treatment planning.

## Features

- **Wound Segmentation**: Accurately identify and outline wound boundaries
- **Wound Classification**: Automatically classify wounds by type (venous ulcer, pressure ulcer, etc.)
- **Measurement Analysis**: Calculate wound area, perimeter, and other metrics
- **Healing Stage Identification**: Determine the current healing stage of the wound
- **LLM-Powered Recommendations**: Generate evidence-based assessment and treatment recommendations
- **Progress Tracking**: Monitor wound healing progress over time
- **Report Generation**: Create comprehensive reports for documentation

## Project Structure

```
SAFEHEAL-DEMO/
├── app/
│   ├── __pycache__/
│   ├── layout.py         # UI layout components
│   ├── main.py           # Main application file
│   └── routes.py         # Page routing logic
├── assets/
│   ├── logo.png          # Application logo
│   └── style.css         # Custom CSS styling
├── backend/
│   ├── __pycache__/
│   ├── gradcam.py        # Grad-CAM visualization for model explainability
│   ├── inference.py      # Model inference code
│   ├── llm_service.py    # LLM integration for recommendations
│   ├── report_generator.py # Report generation utilities
│   └── utils.py          # Utility functions
├── data/
│   ├── uploads/          # Storage for uploaded images
│   └── results/          # Storage for analysis results
├── models/
│   ├── edgenext_wound_classification.pth  # Wound classification model
│   └── updated_unet_edgenext.pth         # Wound segmentation model
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/safeheal.git
   cd safeheal
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run main.py
   ```

## Usage

1. Navigate to the application in your web browser (default: http://localhost:8501)
2. Upload a wound image or capture one using your camera
3. Click "Analyze Wound" to process the image
4. View the segmentation, classification, and AI-generated recommendations
5. Download the analysis report for documentation

## Requirements

- Python 3.8+
- Streamlit
- PyTorch
- OpenCV
- Pillow
- NumPy
- Pandas
- Matplotlib

## Model Information

SafeHeal uses two main deep learning models:

1. **Wound Segmentation**: A U-Net architecture with EdgeNext backbone for accurate wound boundary detection
2. **Wound Classification**: EdgeNext-based model trained to classify wounds into different types

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web application framework
- [PyTorch](https://pytorch.org/) for deep learning capabilities
- [EdgeNext](https://github.com/mmaaz60/EdgeNeXt) for efficient model architecture