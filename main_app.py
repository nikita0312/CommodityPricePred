import streamlit as st
from Dashboard.dashboard import run_dashboard
from commodai.src.commodai.crew import run_crew  # Import your crew.py function
from InferenceApp.app import run_inference  # Import your app.py function

def main():
    # Set page config
    st.set_page_config(
        page_title="Multi-Section Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # Create sidebar
    st.sidebar.title("Navigation")
    
    # Navigation options
    pages = {
        "Dashboard": "📊 Dashboard",
        "Crew Analysis": "👥 Crew Analysis",
        "Inference": "🤖 Inference"
    }
    
    # Default selection
    default_selection = "Dashboard"
    selection = st.sidebar.radio("Go to", list(pages.values()), index=list(pages.keys()).index(default_selection))

    # Display the selected page
    if selection == "📊 Dashboard":
        st.title("Dashboard")
        run_dashboard()
        
    elif selection == "👥 Crew Analysis":
        st.title("Crew Analysis")
        run_crew()
        
    elif selection == "🤖 Inference":
        st.title("Inference")
        run_inference()

    # Add footer to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2024 Your Company Name")

if __name__ == "__main__":
    main()