import streamlit as st
from PIL import Image
import base64
import time

def set_page_config():
    """Set page configuration with title, icon and layout"""
    st.set_page_config(
        page_title="SafeHeal | AI Wound Analysis",
        page_icon="🩹",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better UI with improved contrast
    st.markdown("""
    <style>
        /* Main background and app container */
        .main {
            background-color: #f0f4f8;  /* Lighter blue-gray background */
        }
        .stApp {
            background-color: #f0f4f8;
        }
        .css-1d391kg, .css-12oz5g7 {
            padding-top: 2rem;
        }
        
        /* Typography with improved contrast */
        h1 {
            color: #1a365d !important;  /* Darker blue for better contrast */
            font-weight: 700 !important;
        }
        h2, h3 {
            color: #2a4365 !important;
            font-weight: 600 !important;
        }
        p, li {
            color: #2d3748 !important;  /* Darker text for better readability */
        }
        
        /* Card containers with more distinct shadows */
        .upload-container {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12); 
            margin-bottom: 2.5rem;
            border-top: 5px solid #3182ce;  /* Blue accent border */
        }
        .result-container {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
            margin-bottom: 2.5rem;
            border-top: 5px solid #3182ce;  /* Blue accent border */
        }
        
        /* Button styling with higher contrast */
        .stButton button {
            background-color: #2b6cb0 !important;  /* Darker blue for better contrast */
            color: white !important;
            border-radius: 6px !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }
        .stButton button:hover {
            background-color: #1a4971 !important;  /* Even darker on hover */
            transform: translateY(-2px) !important;
        }
        
        /* Severity indicators with enhanced contrast */
        .severity-high {
            color: #c53030 !important;  /* Darker red */
            font-weight: bold !important;
            background-color: #fed7d7 !important;  /* Light red background */
            padding: 2px 8px !important;
            border-radius: 4px !important;
        }
        .severity-medium {
            color: #c05621 !important;  /* Darker orange */
            font-weight: bold !important;
            background-color: #feebc8 !important;  /* Light orange background */
            padding: 2px 8px !important;
            border-radius: 4px !important;
        }
        .severity-low {
            color: #2f855a !important;  /* Darker green */
            font-weight: bold !important;
            background-color: #c6f6d5 !important;  /* Light green background */
            padding: 2px 8px !important;
            border-radius: 4px !important;
        }
        
        /* Info boxes with better contrast */
        .info-box {
            background-color: #bee3f8;  /* Lighter blue background */
            border-left: 5px solid #2b6cb0;  /* Darker blue border */
            padding: 1.2rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
            color: #2d3748 !important;  /* Darker text for better readability */
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-12oz5g7 {
            background-color: #2a4365 !important;
        }
        .css-1aumxhk, [data-testid="stSidebar"] {
            background-color: #2a4365 !important;
            color: white !important;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] li {
            color: white !important;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: #4a5568;  /* Darker gray for better readability */
            font-size: 0.8rem;
            padding: 1rem;
            background-color: #e2e8f0;
            border-radius: 6px;
        }
        
        /* Custom file uploader */
        .uploadedFile {
            border: 2px dashed #2b6cb0 !important;  /* Darker blue border */
            border-radius: 10px !important;
            padding: 2rem !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #ebf4ff;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2b6cb0 !important;
            color: white !important;
        }
        
        /* Slider improvements */
        .stSlider [data-baseweb=slider] {
            height: 0.5rem !important;
        }
        .stSlider [data-baseweb=thumb] {
            height: 1rem !important;
            width: 1rem !important;
            background-color: #2b6cb0 !important;
        }
        
        /* Progress bar color */
        .stProgress > div > div {
            background-color: #2b6cb0 !important;
        }
        
        /* Checkbox styling */
        .stCheckbox label {
            color: white !important;
        }
        
        /* Select box styling */
        .stSelectbox label {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the app header with logo and title"""
    col1, col2 = st.columns([1, 5])
    
    with col1:
        # Creating a simple logo using SVG
        logo_svg = """
        <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="30" cy="50" r="20" fill="#2B6CB0"/>
        <circle cx="70" cy="50" r="20" fill="#2B6CB0"/>
        <circle cx="50" cy="20" r="20" fill="#2B6CB0"/> 
        <path d="M30 50 L70 50" stroke="white" stroke-width="3"/> 
        <path d="M30 50 L50 20" stroke="white" stroke-width="3"/> 
        <path d="M50 20 L70 50" stroke="white" stroke-width="3"/> 
        </svg>
        """
        st.markdown(logo_svg, unsafe_allow_html=True)
    
    with col2:
        st.title("SafeHeal: AI-Enhanced Wound Analysis")
        st.markdown("""
        <p style="font-size: 1.2rem; color: #4a5568;">Upload a wound image for instant AI analysis, risk assessment, and first aid guidance</p>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1rem 0; background-color: #e2e8f0; height: 2px; border: none;'>", unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with app information and options"""
    with st.sidebar:
        st.header("About SafeHeal")
        st.markdown("""
        <div class="info-box" style="background-color: #4299e1; color: white; border-left-color: white;">
        SafeHeal uses advanced AI to analyze wound images, determine risk levels, 
        and provide appropriate first aid recommendations.
        </div>
        """, unsafe_allow_html=True)
        
        # Add a small illustration using SVG
        workflow_svg = """
        <svg width="100%" height="120" viewBox="0 0 300 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="10" y="40" width="60" height="40" rx="5" fill="#BEE3F8" stroke="#2B6CB0" stroke-width="2"/>
            <text x="40" y="65" font-size="12" text-anchor="middle" fill="#2A4365">Upload</text>
            <path d="M70 60H90" stroke="#2B6CB0" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2"/>
            <rect x="90" y="40" width="60" height="40" rx="5" fill="#BEE3F8" stroke="#2B6CB0" stroke-width="2"/>
            <text x="120" y="65" font-size="12" text-anchor="middle" fill="#2A4365">Analyze</text>
            <path d="M150 60H170" stroke="#2B6CB0" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2"/>
            <rect x="170" y="40" width="60" height="40" rx="5" fill="#BEE3F8" stroke="#2B6CB0" stroke-width="2"/>
            <text x="200" y="65" font-size="12" text-anchor="middle" fill="#2A4365">Results</text>
            <path d="M230 60H250" stroke="#2B6CB0" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2"/>
            <rect x="250" y="40" width="40" height="40" rx="5" fill="#BEE3F8" stroke="#2B6CB0" stroke-width="2"/>
            <text x="270" y="65" font-size="10" text-anchor="middle" fill="#2A4365">Report</text>
        </svg>
        """
        st.markdown(workflow_svg, unsafe_allow_html=True)
        
        st.subheader("How it works")
        st.markdown("""
        1. **Upload** a clear image of the wound
        2. **AI Analysis** detects wound type & severity
        3. **Review** the assessment and recommendations
        4. **Download** a report for medical professionals
        """)
        
        st.markdown("<hr style='margin: 1.5rem 0; background-color: #4299e1; height: 2px; border: none;'>", unsafe_allow_html=True)
        st.subheader("Settings")
        
        analysis_depth = st.select_slider(
            "Analysis Detail Level",
            options=["Basic", "Standard", "Detailed"],
            value="Standard"
        )
        
        show_technical = st.checkbox("Show Technical Details", value=False)
        
        if st.button("Reset Application"):
            st.session_state.clear()
            st.experimental_rerun()
            
        st.markdown("<hr style='margin: 1.5rem 0; background-color: #4299e1; height: 2px; border: none;'>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box" style="background-color: #FC8181; border-left-color: #C53030;">
        <strong>⚠️ Medical Disclaimer:</strong> SafeHeal is designed as a first aid assistant only. 
        Always seek professional medical help for serious injuries.
        </div>
        """, unsafe_allow_html=True)

def render_upload_section():
    """Render the image/video upload section"""
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.subheader("Upload Wound Image or Video")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <p style="color: #4a5568; font-size: 1.05rem;">
        Please upload or capture a clear, well-lit image or video of the wound area. 
        For best results:
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        - Ensure good lighting
        - Remove any bandages or coverings
        - Capture from a straight angle
        - Include some surrounding skin area
        """)
        
        st.radio("Capture Type", ["Image", "Video"], key="capture_type", horizontal=True)
        
        uploaded_file = st.file_uploader(
            "Upload from Device (Image or Video)", 
            type=["jpg", "jpeg", "png", "mp4", "mov", "avi"],
            key="wound_upload"
        )
        
        capture_col1, capture_col2 = st.columns(2)
        with capture_col1:
            if st.button("Capture", key="capture_media"):
                st.session_state.capture_requested = True
        
        with capture_col2:
            if st.button("Use Upload", key="use_upload"):
                st.session_state.capture_requested = False
    
    with col2:
        captured = None

        if 'capture_requested' in st.session_state and st.session_state.capture_requested:
            if st.session_state.capture_type == "Image":
                captured = st.camera_input("Capture an Image")
                if captured:
                    st.session_state.captured_media = captured
            else:
                st.warning("Video capture is not natively supported in Streamlit's camera_input.")
                st.info("Please upload a video instead if you wish to use video.")
        
        if uploaded_file is not None:
            file_type = uploaded_file.type
            if "image" in file_type:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                st.session_state.analyzed_image = uploaded_file
            elif "video" in file_type:
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                st.video(tfile.name)
                st.session_state.analyzed_video = tfile.name
        
        elif 'captured_media' in st.session_state:
            captured_file = st.session_state.captured_media
            image = Image.open(captured_file)
            st.image(image, caption="Captured Image", use_container_width=True)
            st.session_state.analyzed_image = captured_file
        
        else:
            # Placeholder
            st.markdown("""
            <div style="
                border: 2px dashed #90cdf4;
                border-radius: 10px;
                padding: 4rem 2rem;
                text-align: center;
                color: #4a5568;
                background-color: #ebf8ff;
                margin-top: 1rem;
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#4a5568" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
                <p style="margin-top: 1rem; font-size: 1.1rem; color: #4a5568;">Preview will appear here</p>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.get("analyzed_image") or st.session_state.get("analyzed_video"):
        if st.button("Analyze Media", key="analyze_btn"):
            st.session_state.run_analysis = True

    st.markdown('</div>', unsafe_allow_html=True)


def render_results_section(segmented_image=None, wound_class=None, risk_level=None, recommendations=None, explanation=None):
    """Render the results section with analysis and recommendations"""
    if not ('run_analysis' in st.session_state and st.session_state.run_analysis):
        return
    
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    st.subheader("Analysis Results")
    
    # Progress indicator during analysis
    if 'analysis_complete' not in st.session_state:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate analysis progress
        for i in range(101):
            if i < 30:
                status_text.text("Segmenting wound area...")
            elif i < 60:
                status_text.text("Classifying wound type...")
            elif i < 90:
                status_text.text("Generating recommendations...")
            else:
                status_text.text("Finalizing analysis...")
            
            progress_bar.progress(i)
            time.sleep(0.02)
        
        status_text.text("Analysis complete!")
        st.session_state.analysis_complete = True
        time.sleep(1)
        st.experimental_rerun()
    
    if 'analysis_complete' in st.session_state:
        tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Analysis", "First Aid Guide"])
        
        # Sample data - in real app, this would come from your backend
        if not wound_class:
            wound_class = "Laceration (Cut)"
        if not risk_level:
            risk_level = "Medium"
        if not recommendations:
            recommendations = [
                "Clean the wound with mild soap and water",
                "Apply gentle pressure with a clean cloth to stop bleeding",
                "Apply antibiotic ointment if available",
                "Cover with a sterile bandage",
                "Seek medical attention if the cut is deep or shows signs of infection"
            ]
        if not explanation:
            explanation = "This appears to be a laceration with moderate depth. There is minimal tissue damage visible, but proper cleaning and dressing is recommended to prevent infection. The edges of the wound are relatively clean which suggests good healing potential with appropriate care."
        
        with tab1:
            col1, col2 = st.columns([3, 2])
            
            with col1:
                if segmented_image:
                    st.image(segmented_image, caption="Wound Analysis", use_container_width=True)
                else:
                    # Use the uploaded image with a simulated overlay
                    uploaded_img = Image.open(st.session_state.analyzed_image)
                    
                    # Display the image with caption
                    st.image(uploaded_img, caption="Wound Analysis", use_container_width=True)
                    
                    # Explain that segmentation would appear here
                    st.info("In the full version, AI wound segmentation would be displayed as an overlay")
                
            with col2:
                st.markdown("### Summary")
                st.markdown(f"**Wound Type:** {wound_class}")
                
                severity_class = ""
                if risk_level == "High":
                    severity_class = "severity-high"
                elif risk_level == "Medium":
                    severity_class = "severity-medium"
                else:
                    severity_class = "severity-low"
                
                st.markdown(f"""
                **Risk Level:** <span class="{severity_class}">{risk_level}</span>
                """, unsafe_allow_html=True)
                
                st.markdown("### Key Recommendations")
                for rec in recommendations[:3]:
                    st.markdown(f"- {rec}")
                
                if risk_level == "High":
                    st.warning("⚠️ Seek immediate medical attention!")
                elif risk_level == "Medium":
                    st.info("Consider consulting a healthcare provider")
                
                st.markdown("### AI Assessment")
                st.markdown(explanation)
            
        with tab2:
            st.markdown("### Technical Analysis")
            
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            with metrics_col1:
                st.metric("Wound Area", "3.2 cm²")
            with metrics_col2:
                st.metric("Depth Est.", "Medium")
            with metrics_col3:
                st.metric("Infection Risk", "18%")
            
            st.markdown("### Wound Characteristics")
            st.markdown("""
            | Feature | Assessment |
            | --- | --- |
            | Edges | Clean, slightly irregular |
            | Tissue Loss | Minimal |
            | Bleeding | Controlled |
            | Contamination | Low-Medium |
            | Inflammation | Minimal |
            """)
            
            st.markdown("### Classification Confidence")
            st.progress(0.87)
            st.caption("87% confidence in classification")
            
            # Add a GradCAM visualization with SVG
            st.markdown("### Visual Analysis (Grad-CAM)")
            
            gradcam_svg = """
            <svg width="100%" height="200" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="200" rx="10" fill="#E2E8F0"/>
                <ellipse cx="200" cy="100" rx="150" ry="70" fill="#FED7D7" opacity="0.7"/>
                <ellipse cx="200" cy="100" rx="100" ry="50" fill="#FC8181" opacity="0.6"/>
                <ellipse cx="200" cy="100" rx="50" ry="30" fill="#F56565" opacity="0.8"/>
                <path d="M190 100C190 100 200 120 210 100" stroke="#C53030" stroke-width="3"/>
                <text x="150" y="40" font-size="14" fill="#2D3748">Higher attention area</text>
                <path d="M150 45L120 80" stroke="#2D3748" stroke-width="1" stroke-dasharray="2 2"/>
            </svg>
            """
            st.markdown(gradcam_svg, unsafe_allow_html=True)
            st.caption("Heatmap showing areas of concern in the wound analysis")
        
        with tab3:
            st.markdown("### First Aid Instructions")
            
            # Add a first aid instruction image using SVG
            first_aid_svg = """
            <svg width="300" height="200" viewBox="0 0 300 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="300" height="200" rx="10" fill="#E2E8F0"/>
                <circle cx="150" cy="100" r="70" fill="white" stroke="#2B6CB0" stroke-width="2"/>
                <rect x="125" y="75" width="50" height="50" rx="5" fill="white" stroke="#2B6CB0" stroke-width="2"/>
                <path d="M125 100H175" stroke="#2B6CB0" stroke-width="4"/>
                <path d="M150 75V125" stroke="#2B6CB0" stroke-width="4"/>
                <path d="M80 160C80 140 90 130 150 130C210 130 220 140 220 160" stroke="#2B6CB0" stroke-width="2" stroke-dasharray="3 3"/>
                <circle cx="80" cy="170" r="10" fill="#BEE3F8"/>
                <circle cx="220" cy="170" r="10" fill="#BEE3F8"/>
                <text x="150" y="180" font-size="14" text-anchor="middle" fill="#2D3748">First Aid Kit</text>
            </svg>
            """
            st.markdown(first_aid_svg, unsafe_allow_html=True)
            
            steps = []
            for i, rec in enumerate(recommendations):
                steps.append(f"**Step {i+1}:** {rec}")
            
            st.markdown("\n\n".join(steps))
            
            st.markdown("### When to Seek Medical Help")
            st.markdown("""
            - If bleeding cannot be controlled after 15 minutes of pressure
            - If the wound is very deep, jagged, or gaping
            - If there are signs of infection (increasing redness, warmth, swelling, pus)
            - If you cannot properly clean the wound
            - If the wound was caused by a rusty or dirty object
            - If you haven't had a tetanus shot in the last 5 years
            """)
        
        st.markdown("<hr style='margin: 1.5rem 0; background-color: #e2e8f0; height: 2px; border: none;'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            if st.button("Download PDF Report"):
                st.info("Preparing PDF report for download...")
                # This would trigger report generation in your backend
        
        with col2:
            if st.button("Save to Health Record"):
                st.success("Analysis saved to health record")
                # This would trigger saving to a database
        
        with col3:
            if st.button("New Analysis"):
                # Reset the relevant session state variables
                st.session_state.run_analysis = False
                st.session_state.analysis_complete = False
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Render the footer with copyright and disclaimer"""
    st.markdown("""
    <div class="footer">
        <p>© 2025 SafeHeal. All rights reserved.</p>
        <p>SafeHeal is not a substitute for professional medical advice, diagnosis, or treatment.</p>
        <p>Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
        <p>Never disregard professional medical advice or delay in seeking it because of something you have read on this site.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Set up the page
    set_page_config()
    
    # Initialize session state if needed
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
        st.session_state.run_analysis = False
        st.session_state.analysis_complete = False
    
    # Render all UI components
    render_header()
    render_sidebar()
    render_upload_section()
    render_results_section()
    render_footer()

if __name__ == "__main__":
    main()