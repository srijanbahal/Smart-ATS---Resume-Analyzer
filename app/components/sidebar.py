import streamlit as st
from config import reset_session_state

def render_sidebar():
    """Render the sidebar with file upload and input fields"""
    with st.sidebar:
        st.title("📝 Smart ATS")
        st.subheader("Upload Your Documents")
        
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type="pdf",
            help="Please upload your resume in PDF format"
        )
        
        jd = st.text_area("Job Description", height=200)
        github_username = st.text_input("GitHub Username (Optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.button("Analyze")
        with col2:
            clear = st.button("Clear")
            
        if clear:
            reset_session_state()
            st.rerun()
            
        return uploaded_file, jd, github_username, submit 