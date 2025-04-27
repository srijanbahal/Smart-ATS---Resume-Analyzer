import streamlit as st
import json
import os
from config import setup_page, init_session_state
from utils.pdf_utils import extract_text_from_pdf
from utils.github_utils import fetch_github_data
from models.gemini import analyze_resume
from components.display import display_results
from components.sidebar import render_sidebar
from utils.logging_utils import default_logger as logger

def main():
    # Setup page and initialize session state
    setup_page()
    init_session_state()
    
    logger.info("Application started")
    
    # Render sidebar and get inputs
    uploaded_file, jd, github_username, submit = render_sidebar()
    
    # Main content area
    if not st.session_state.current_state['analysis_complete'] and not submit:
        # Landing page content
        st.title("🚀 Welcome to Smart ATS")
        st.markdown("""
        ### Enhance Your Job Application with AI-Powered Analysis
        
        Upload your resume and job description to:
        - 📊 Get ATS compatibility score
        - 🎯 Identify missing keywords
        - 📋 Receive personalized improvement suggestions
        
        **Plus:** Add your GitHub username for comprehensive project analysis!
        """)
        return

    if submit:
        if not uploaded_file or not jd:
            logger.warning("Missing required inputs: resume or job description")
            st.error("Please upload your resume and provide the job description.")
            return
        
        logger.info("Starting resume analysis")
        with st.spinner("Analyzing your resume..."):
            # Extract text from PDF
            logger.debug(f"Processing PDF file: {uploaded_file.name}")
            logger.info("Extracting text from PDF")

            text = extract_text_from_pdf(uploaded_file)

            if not text:
                logger.error("Failed to extract text from PDF")
                st.error("Could not extract text from the PDF. Please check the file.")
                return
            
            # Fetch GitHub data if username provided
            github_data = None
            if github_username:
                logger.info(f"Fetching GitHub data for {github_username}")
                with st.spinner("Fetching GitHub data..."):
                    github_data = fetch_github_data(github_username)
                    if not github_data:
                        logger.warning(f"No public repositories found for user {github_username}")
                        st.warning(f"No public repositories found for user {github_username}")
            
            # Process the resume and update state
            logger.info("Analyzing resume")
            response = analyze_resume(text, jd, github_username if github_data else None)
            if response:
                try:
                    response_dict = json.loads(response)
                    st.session_state.current_state.update({
                        'analysis_complete': True,
                        'response_dict': response_dict,
                        'github_data': github_data['repositories'] if github_data else None,
                        'include_github': bool(github_data)
                    })
                except Exception as e:
                    logger.error(f"Failed to parse analysis response: {str(e)}")
                    st.error("An error occurred while analyzing your resume. Please try again.")
                    return

    # Display results if analysis is complete
    if st.session_state.current_state['analysis_complete']:
        logger.info("Displaying analysis results")
        display_results(
            st.session_state.current_state['response_dict'],
            st.session_state.current_state['github_data'],
            st.session_state.current_state['include_github']
        )

if __name__ == "__main__":
    main() 