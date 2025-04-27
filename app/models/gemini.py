import google.generativeai as genai
import streamlit as st
from config import GOOGLE_API_KEY
from prompts.templates import ats_prompt, github_analysis_prompt

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

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
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error getting Gemini response: {str(e)}")
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