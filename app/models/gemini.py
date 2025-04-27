import google.generativeai as genai
import streamlit as st
from config import GOOGLE_API_KEY
from prompts.templates import ats_prompt, github_analysis_prompt
from utils.logging_utils import default_logger as logger

# Configure Gemini
try:
    if not GOOGLE_API_KEY:
        logger.error("Gemini API key not found in environment variables")
        st.error("Please set up your Gemini API key in the app settings")
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    st.error("Error configuring Gemini API. Please check your API key.")

@st.cache_data(ttl=3600)
def get_gemini_response(input_prompt):
    """
    Get response from Gemini model with caching
    
    Args:
        input_prompt (str): Formatted prompt for the model
    
    Returns:
        str: Model's response text
    """
    try:
        if not GOOGLE_API_KEY:
            logger.error("Cannot generate response: Gemini API key not configured")
            return None
            
        logger.debug("Creating Gemini model instance")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        logger.debug("Generating content with prompt")
        response = model.generate_content(input_prompt)
        
        logger.debug("Successfully generated response")
        return response.text
        
    except Exception as e:
        error_msg = f"Error getting Gemini response: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)
        return None

def analyze_resume(text, jd, github_data=None):
    """
    Analyze resume with or without GitHub data
    
    Args:
        text (str): Resume text
        jd (str): Job description
        github_data (dict, optional): GitHub repository data
    
    Returns:
        str: JSON response string from Gemini, or None if analysis fails
    """
    try:
        if github_data:
            prompt = github_analysis_prompt.format(
                text=text,
                jd=jd,
                github_data=github_data
            )
        else:
            prompt = ats_prompt.format(
                text=text,
                jd=jd
            )
        
        response = get_gemini_response(prompt)
        if not response:
            return None
            
        # Clean the response
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:-3]
            
        return response
        
    except Exception as e:
        st.error(f"Error in resume analysis: {str(e)}")
        return None 