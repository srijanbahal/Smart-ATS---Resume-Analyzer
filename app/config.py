import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Page configuration
def setup_page():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="Smart ATS - Resume Analyzer",
        page_icon="📝",
        layout="wide"
    )

# Session state initialization
def init_session_state():
    """Initialize the session state if not already done"""
    if 'current_state' not in st.session_state:
        st.session_state.current_state = {
            'analysis_complete': False,
            'response_dict': None,
            'github_data': None,
            'include_github': False,
            'resume_text': None,
            'jd_text': None
        }

def reset_session_state():
    st.session_state.current_state = {
        'analysis_complete': False,
        'response_dict': None,
        'github_data': None,
        'include_github': False,
        'resume_text': None,
        'jd_text': None
    } 