import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Jd and the missing keywords with high accuracy.

resume: {text}
description: {jd}

Strictly provide the response in the following JSON format without any additional text or explanation:
{{
    "JD Match": "X%",
    "MissingKeywords": ["keyword1", "keyword2", ...],
    "Profile Summary": "detailed summary here"
}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt.format(text=text, jd=jd))
        
        # Parse the JSON response
        try:
            # Clean the response string
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:-3]  # Remove ```json and ``` markers
            
            response_dict = json.loads(response)
            
            # Display JD Match with a metric
            st.header("Resume Analysis Results")
            
            # Create columns for layout
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Remove the % symbol if it exists in the string
                match_percentage = response_dict["JD Match"].replace("%", "")
                st.metric(
                    label="JD Match",
                    value=f"{match_percentage}%",
                    delta=None
                )
            
            # Display Missing Keywords section
            st.subheader("Missing Keywords")
            if response_dict["MissingKeywords"]:
                missing_keywords = response_dict["MissingKeywords"]
                # Create a more visually appealing display of keywords
                cols = st.columns(3)
                for i, keyword in enumerate(missing_keywords):
                    cols[i % 3].markdown(f"- {keyword}")
            else:
                st.success("No missing keywords found!")
            
            # Display Profile Summary
            st.subheader("Profile Summary")
            st.info(response_dict["Profile Summary"])
            
            # Add improvement suggestions
            if float(match_percentage) < 85:
                st.warning("⚠️ Consider adding the missing keywords to improve your resume match score.")
                
        except json.JSONDecodeError as e:
            st.error("Error parsing the response. Please try again.")
            with st.expander("Show detailed error"):
                st.code(response)
                st.text(str(e))