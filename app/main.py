# app/main.py

import streamlit as st
# from app import layout, routes
import layout
import routes


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "History", "Settings"])

if page == "Home":
    if 'input_data' in st.session_state:
        routes.home()
    else:
        layout
elif page == "About":
    routes.about()
elif page == "History":
    routes.history()
elif page == "Settings":
    routes.settings()

st.markdown("<div class='footer'>SafeHeal v1.0 — Developed with ❤️ for Healthcare AI</div>", unsafe_allow_html=True)
