import streamlit as st


def main():
    # Set page config
    st.set_page_config(
        page_title="Multi-Section Dashboard", page_icon="📊", layout="wide"
    )

    st.title("Welcome to the Dashboard")
    st.markdown(
        """
    Welcome to our multi-section dashboard. Use the sidebar to navigate between:
    - 📊 Dashboard
    - 👥 Crew Analysis
    - 🤖 Inference
    """
    )

    # Add footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2024 Your Company Name")


if __name__ == "__main__":
    main()
