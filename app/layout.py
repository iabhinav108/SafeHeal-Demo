import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="SafeHeal - AI Wound Analysis",
    page_icon="🩹",
    layout="wide",
    initial_sidebar_state="expanded"
)

css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .main-header {color: #2c3e50; margin-bottom: 0;}
    .sub-header {color: #34495e; margin-top: 0; font-size: 1.2rem;}
    .description {margin: 20px 0; font-size: 1.1rem;}
    .footer {margin-top: 50px; text-align: center; color: #7f8c8d; font-size: 0.8rem;}
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    try:
        logo = Image.open("assets/logo.png")
        st.image(logo, width=70)
    except:
        st.markdown("🩹")  # Fallback emoji if image loading fails
        
with col2:
    st.markdown("<h1 class='main-header'>SafeHeal</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>AI-Powered Wound Segmentation & Classification with LLM Support</h2>", unsafe_allow_html=True)

st.markdown(
    "<div class='description'>SafeHeal leverages AI to assist in wound segmentation, classification, and provides intelligent care recommendations. Get started below!</div>",
    unsafe_allow_html=True
)

media_type = st.radio(
    label="Select Analysis Type:",
    options=["Image"],
    horizontal=True
)

if 'image_input' not in st.session_state:
    st.session_state.image_input = None

if media_type == "Image":
    st.markdown("#### Upload or Capture an Image")
    method = st.radio(
        label="Choose Input Method:",
        options=["Upload Image", "Capture Image"],
        horizontal=True
    )

    if method == "Upload Image":
        uploaded_image = st.file_uploader(
            label="Upload Image",
            type=["jpg", "jpeg", "png"],
            key="uploader"
        )
        if uploaded_image is not None:
            st.session_state.image_input = uploaded_image
            
    else:
        captured = st.camera_input(
            label="Capture Image",
            key="camera"
        )
        if captured is not None:
            st.session_state.image_input = captured
    
    if st.session_state.image_input is not None:
        try:
            img = Image.open(st.session_state.image_input)
            st.image(img, caption="Selected Image", use_column_width=True)
            
            if st.button("Segment and Classify Disease"):
                st.success("Processing image for wound segmentation and classification...")
                # results = process_image(st.session_state.image_input)
                # display_results(results)
        except Exception as e:
            st.error(f"Error processing image: {e}")
            st.session_state.image_input = None

st.markdown(
    "<div class='footer'>SafeHeal v1.0 — Empowering Advanced Wound Care with AI</div>",
    unsafe_allow_html=True
)