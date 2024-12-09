#!/usr/bin/env python
import warnings
import streamlit as st
from crew import Commodai
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

REPORT_PATH = "./report.md"


# Define the Streamlit UI
def run_streamlit_ui():
    st.set_page_config(
        page_title="CommodAI Topic Analysis",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Custom styling for a polished look
    st.markdown(
        """
        <style>
        .main {
            background-color: #f8f9fa;
            color: #333;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App Title
    st.title("🌾 CommodAI Crew Runner")

    # Input form
    st.markdown("### Enter a Topic for Analysis")
    topic = st.text_input(
        "Topic:",
        placeholder="Type a topic, e.g., Rice Production",
        help="Enter the topic you want CommodAI to analyze.",
    )

    if st.button("Run Analysis"):
        if topic.strip():
            st.markdown("### Results:")
            st.info(f"Running analysis for topic: **{topic}**")

            # Add a spinner while the analysis is running
            with st.spinner("Performing analysis, please wait..."):
                try:
                    # Call CommodAI with the user-input topic
                    inputs = {"topic": topic}
                    Commodai().crew().kickoff(inputs=inputs)

                    # Check if the report file exists and display its contents
                    if os.path.exists(REPORT_PATH):
                        st.success(
                            "Analysis completed successfully! Here's the report:"
                        )
                        with open(REPORT_PATH, "r") as report_file:
                            report_content = report_file.read()
                        st.markdown(report_content, unsafe_allow_html=True)
                    else:
                        st.warning("The report.md file was not found.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    run_streamlit_ui()
