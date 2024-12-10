import streamlit as st
from Dashboard.dashboard import run_dashboard
from commodai.src.commodai.main import run_streamlit_ui
import subprocess
import os
import sys


def main():
    # Set page config
    st.set_page_config(
        page_title="Multi-Section Dashboard", page_icon="📊", layout="wide"
    )

    # Create sidebar
    st.sidebar.title("Navigation")

    # Navigation options
    pages = {
        "Dashboard": "📊 Dashboard",
        "Crew Analysis": "👥 Crew Analysis",
        "Inference": "🤖 Inference",
    }

    # Default selection
    default_selection = "Dashboard"
    selection = st.sidebar.radio(
        "Go to", list(pages.values()), index=list(pages.keys()).index(default_selection)
    )

    # Display the selected page
    if selection == "📊 Dashboard":
        st.title("Dashboard")
        run_dashboard()

    elif selection == "👥 Crew Analysis":

        # Import and run the streamlit UI function directly
        crew_path = os.path.join("commodai", "src", "commodai")
        sys.path.append(crew_path)
        try:
            run_streamlit_ui()
        except Exception as e:
            st.error(f"Error running crew analysis: {str(e)}")

    elif selection == "🤖 Inference":
        st.title("Inference")
        # Run the entire app.py file from InferenceApp
        inference_path = os.path.join("InferenceApp", "app.py")
        try:
            subprocess.run(["python", inference_path], check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Error running inference: {str(e)}")

    # Add footer to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2024 Your Company Name")


if __name__ == "__main__":
    main()
