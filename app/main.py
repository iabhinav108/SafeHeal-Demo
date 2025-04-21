import streamlit as st
import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import from your project structure
from app.layout import (
    set_page_config, 
    render_header, 
    render_sidebar, 
    render_upload_section, 
    render_results_section, 
    render_footer
)
from app.routes import process_image, generate_report
from backend.inference import load_models, run_inference
from backend.llm_service import initialize_llm

def main():
    """Main entry point for the SafeHeal Streamlit application"""
    
    # Set up page configuration and styles
    set_page_config()
    
    # Initialize session state if needed
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
        st.session_state.run_analysis = False
        st.session_state.analysis_complete = False
    
    # Display components
    render_header()
    render_sidebar()
    
    # Load models in background
    if not st.session_state.models_loaded:
        with st.spinner("Loading AI models..."):
            try:
                # These would be your actual model loading functions
                # segmentation_model, classification_model = load_models()
                # llm = initialize_llm()
                
                # For demo purposes:
                st.session_state.models_loaded = True
                
                # Store models in session state
                # st.session_state.segmentation_model = segmentation_model
                # st.session_state.classification_model = classification_model
                # st.session_state.llm = llm
            except Exception as e:
                st.error(f"Error loading models: {str(e)}")
                st.stop()
    
    # Upload section
    render_upload_section()
    
    # Results section - will only show when analysis is triggered
    if 'run_analysis' in st.session_state and st.session_state.run_analysis:
        # In a real application, you would process the image here
        # segmented_image, wound_class, risk_level, recommendations, explanation = process_image(
        #    st.session_state.analyzed_image,
        #    st.session_state.segmentation_model,
        #    st.session_state.classification_model,
        #    st.session_state.llm
        # )
        
        # For demo purposes, pass None for these (the layout function has defaults)
        render_results_section()
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()