import streamlit as st
from commodai.src.commodai.main import run_streamlit_ui

try:
    run_streamlit_ui()
except Exception as e:
    st.error(f"Error running crew analysis: {str(e)}")
