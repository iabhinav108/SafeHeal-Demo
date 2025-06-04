# app/routes.py

import streamlit as st
from PIL import Image
import pandas as pd
import time

def home():
    st.header("Home - Analyze Wound")

    if 'input_data' not in st.session_state or 'media_type' not in st.session_state:
        st.warning("Please select an image or video first from the Home page.")
        return

    media_type = st.session_state['media_type']
    input_data = st.session_state['input_data']

    if media_type == 'image':
        img = Image.open(input_data)
        st.image(img, caption="Analyzing Uploaded Image", use_column_width=True)

        with st.spinner('Analyzing wound image...'):
            time.sleep(2)

        st.success("Wound Segmentation and Classification Completed!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Segmentation Result")
            st.image(img, caption="Segmented Wound (Simulated)", use_column_width=True)
            st.metric(label="Wound Area", value="12.4 cm²")
            st.metric(label="Wound Perimeter", value="14.8 cm")

        with col2:
            st.subheader("Classification Result")
            wound_types = pd.DataFrame({
                "Wound Type": ["Abrasion", "Burn", "Diabetic Wound"],
                "Confidence": [0.78, 0.15, 0.07]
            })
            st.bar_chart(wound_types.set_index("Wound Type"))

            st.subheader("Healing Stage")
            st.info("Inflammatory Phase (Early)")

    elif media_type == 'video':
        st.video(input_data)

        st.info("Note: Video frame extraction and wound detection will be processed in the backend. Coming soon!")

def about():
    st.header("About SafeHeal")

    st.markdown("""
    **SafeHeal** is an AI-powered wound assessment platform combining computer vision and language models.
    
    **Features:**
    - Wound Segmentation
    - Wound Type Classification
    - Healing Stage Analysis
    - Treatment Recommendations

    **Technologies:**
    - Deep Learning (PyTorch, TensorFlow)
    - Computer Vision (OpenCV)
    - NLP (LLMs)
    - Streamlit for Web UI
    """)

def history():
    st.header("Patient History")

    st.info("Login to view previous analyses and patient wound history.")
    
    with st.expander("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Placeholder login validation
            if username == "admin" and password == "admin":
                st.success("Login successful!")
                st.dataframe({
                    "Date": ["2025-04-20", "2025-04-15"],
                    "Patient ID": ["P001", "P002"],
                    "Wound Type": ["Burn", "Diabetic Ulcer"],
                    "Healing Stage": ["Granulation", "Inflammatory"],
                    "Comments": ["Healing well", "Monitor infection risk"]
                })
            else:
                st.error("Invalid credentials.")

def settings():
    st.header("Settings")

    st.subheader("AI Model Settings")
    st.slider("Segmentation Confidence Threshold", 0.0, 1.0, 0.5)
    st.slider("Classification Confidence Threshold", 0.0, 1.0, 0.7)

    st.subheader("Display Settings")
    st.checkbox("Show detailed wound measurements", value=True)
    st.checkbox("Show LLM-generated recommendations", value=True)

    st.subheader("Export Settings")
    st.selectbox("Preferred export format", ["PDF", "CSV", "JSON"])

    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
