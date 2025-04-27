import PyPDF2 as pdf
import streamlit as st

@st.cache_data(ttl=3600)
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from uploaded PDF file
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        str: Extracted text from PDF
    """
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None 