import streamlit as st
import warnings


warnings.filterwarnings("ignore")


# Import and run the dashboard
from InferenceApp.app import main

main()
