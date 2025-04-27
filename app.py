import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import plotly.express as px
import pandas as pd
from github_repo_fecth import GithubRepoFetcher

# Page configuration
st.set_page_config(
    page_title="Smart ATS - Resume Analyzer",
    page_icon="📝",
    layout="wide"
)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt templates
ats_prompt = """
Analyze the resume against the job description as an experienced ATS system with deep understanding of tech field, 
software engineering, data science, data analysis, and big data engineering. Consider the competitive job market 
and provide detailed feedback.

Resume: {text}
Job Description: {jd}

Provide the response in the following JSON format without any additional text:
{{
    "JD Match": "X%",
    "MissingKeywords": ["keyword1", "keyword2", ...],
    "Profile Summary": "detailed summary here"
}}
"""

github_analysis_prompt = """
Analyze the resume, job description, and GitHub projects to provide comprehensive feedback.
Pay special attention to the GitHub projects and how they can enhance the resume.

Resume: {text}
Job Description: {jd}
GitHub Projects: {github_data}

Consider the following for each project:
1. Technical skills demonstrated
2. Relevance to the job description
3. Project complexity and impact
4. How it can be presented in the resume

Provide the response in the following JSON format without any additional text:
{{
    "JD Match": "X%",
    "MissingKeywords": ["keyword1", "keyword2", ...],
    "Profile Summary": "detailed summary here",
    "GitHub Analysis": {{
        "RecommendedProjects": [
            {{
                "ProjectName": "name",
                "Relevance": "X%",
                "RecommendedDescription": "how to present this project in resume",
                "KeySkills": ["skill1", "skill2", ...],
                "ImpactScore": "X/10"
            }}
        ],
        "OverallGitHubScore": "X/10",
        "Recommendations": "specific recommendations for improving GitHub profile"
    }}
}}
"""

def create_keyword_chart(keywords):
    if not keywords:
        return None
    df = pd.DataFrame({
        'Keyword': keywords,
        'Count': [1] * len(keywords)
    })
    fig = px.bar(df, x='Keyword', y='Count', title='Missing Keywords')
    fig.update_layout(showlegend=False)
    return fig

def create_project_relevance_chart(projects):
    df = pd.DataFrame([
        {
            'Project': p['ProjectName'],
            'Relevance': float(p['Relevance'].strip('%')),
            'Impact': float(p['ImpactScore'].split('/')[0])
        } for p in projects
    ])
    
    fig = px.bar(df, x='Project', y=['Relevance', 'Impact'],
                 title='Project Relevance and Impact',
                 barmode='group')
    return fig

def create_keyword_table(keywords):
    if not keywords:
        return None
    df = pd.DataFrame({
        'Missing Keywords': keywords,
        'Impact': ['High'] * len(keywords),
        'Suggested Implementation': [
            'Add to Skills/Technologies section' if 'framework' in kw.lower() or 'language' in kw.lower() or 'tool' in kw.lower()
            else 'Include in Work Experience' if 'experience' in kw.lower() or 'year' in kw.lower()
            else 'Add to Project Highlights' if 'project' in kw.lower() or 'develop' in kw.lower()
            else 'General Addition'
            for kw in keywords
        ]
    })
    return df

def create_skill_match_chart(response_dict):
    # Extract skill categories and their match percentages
    skills_data = {
        'Technical Skills': float(response_dict['JD Match'].replace('%', '')),
        'Project Experience': float(response_dict.get('ProjectMatch', '60').replace('%', '')),
        'Work Experience': float(response_dict.get('WorkExpMatch', '70').replace('%', '')),
        'Education': float(response_dict.get('EduMatch', '80').replace('%', '')),
    }
    
    df = pd.DataFrame({
        'Category': list(skills_data.keys()),
        'Match Percentage': list(skills_data.values())
    })
    
    fig = px.bar(df, x='Category', y='Match Percentage',
                 title='Resume Component Match Analysis',
                 labels={'Match Percentage': 'Match %'},
                 color='Match Percentage',
                 color_continuous_scale='viridis')
    
    fig.update_layout(yaxis_range=[0, 100])
    return fig

def display_github_project(project, languages, stars, forks):
    with st.expander(f"📂 {project['ProjectName']} - Relevance: {project['Relevance']}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Recommended Description:**")
            st.write(project['RecommendedDescription'])
            
            st.write("**Key Skills:**")
            skills_cols = st.columns(3)
            for i, skill in enumerate(project['KeySkills']):
                skills_cols[i % 3].markdown(f"- {skill}")
        
        with col2:
            st.metric("Impact Score", project['ImpactScore'])
            if languages:
                st.write("**Languages:**")
                for lang, percentage in languages.items():
                    st.write(f"- {lang}: {percentage}%")
            st.metric("Stars", stars)
            st.metric("Forks", forks)

def display_improvement_suggestions(response_dict, github_data=None):
    st.subheader("📈 Resume Improvement Suggestions")
    
    # Create tabs for different types of suggestions
    tabs = st.tabs(["General Improvements", "Skills Enhancement", "Project Highlights"])
    
    with tabs[0]:
        st.markdown("### General Suggestions")
        st.markdown("""
        1. **Format and Structure**
           - Use clear section headings
           - Maintain consistent formatting
           - Keep to 1-2 pages
           
        2. **Content Organization**
           - Place most relevant experience first
           - Use bullet points for clarity
           - Quantify achievements where possible
        """)
        
        if float(response_dict['JD Match'].replace('%', '')) < 85:
            st.warning("⚠️ Your resume needs significant alignment with the job requirements")
    
    with tabs[1]:
        st.markdown("### Skills to Highlight")
        missing_skills = response_dict.get('MissingKeywords', [])
        if missing_skills:
            st.markdown("**Add these key skills:**")
            cols = st.columns(2)
            for i, skill in enumerate(missing_skills):
                cols[i % 2].markdown(f"- {skill}")
    
    with tabs[2]:
        st.markdown("### Project Recommendations")
        if github_data:
            st.markdown("**GitHub Projects to Highlight:**")
            for repo in github_data[:3]:  # Show top 3 relevant projects
                with st.expander(f"🔍 {repo['name']}"):
                    st.markdown(f"**Description:** {repo['description']}")
                    st.markdown("**Suggested Bullet Points:**")
                    st.markdown(f"- Developed {repo['name']} using {', '.join(list(repo['languages'].keys())[:3])}")
                    st.markdown(f"- Implemented features resulting in {repo['stars']} stars and {repo['forks']} forks")

def display_results(response_dict, github_data=None, include_github=False):
    # Display JD Match with a metric
    st.header("📊 Resume Analysis Results")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        match_percentage = response_dict["JD Match"].replace("%", "")
        st.metric(
            label="JD Match",
            value=f"{match_percentage}%",
            delta=None
        )
    
    # Display skill match chart
    fig_skills = create_skill_match_chart(response_dict)
    st.plotly_chart(fig_skills, use_container_width=True)
    
    # Display Missing Keywords section with switchable view
    st.subheader("🎯 Missing Keywords")
    if response_dict["MissingKeywords"]:
        view_type = st.radio(
            "Select View",
            ["Graph View", "Table View"],
            horizontal=True,
            key="keywords_view"
        )
        
        if view_type == "Graph View":
            fig = create_keyword_chart(response_dict["MissingKeywords"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:  # Table View
            df = create_keyword_table(response_dict["MissingKeywords"])
            if df is not None:
                st.dataframe(
                    df,
                    column_config={
                        "Missing Keywords": st.column_config.TextColumn("Missing Keywords", width="medium"),
                        "Impact": st.column_config.TextColumn("Impact Level", width="small"),
                        "Suggested Implementation": st.column_config.TextColumn("Where to Add", width="large")
                    },
                    use_container_width=True
                )
    else:
        st.success("No missing keywords found!")
    
    # Display Profile Summary
    st.subheader("📋 Profile Summary")
    st.info(response_dict["Profile Summary"])
    
    # Display GitHub Analysis if available
    if include_github and "GitHub Analysis" in response_dict:
        st.header("🐙 GitHub Projects Analysis")
        github_analysis = response_dict["GitHub Analysis"]
        
        # Display overall GitHub score
        if "OverallGitHubScore" in github_analysis:
            st.metric("Overall GitHub Profile Score", github_analysis["OverallGitHubScore"])
        
        # Display recommendations
        if "Recommendations" in github_analysis:
            st.info(github_analysis["Recommendations"])
        
        # Create project relevance chart
        if "RecommendedProjects" in github_analysis:
            fig = create_project_relevance_chart(github_analysis["RecommendedProjects"])
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed project information
            for project in github_analysis["RecommendedProjects"]:
                # Find matching GitHub data
                github_project = next(
                    (p for p in github_data if p["name"] == project["ProjectName"]),
                    {"languages": {}, "stars": 0, "forks": 0}
                )
                display_github_project(
                    project,
                    github_project.get("languages", {}),
                    github_project.get("stars", 0),
                    github_project.get("forks", 0)
                )
    
    # Display improvement suggestions
    display_improvement_suggestions(response_dict, github_data)

# Main UI
def main():
    # Sidebar
    with st.sidebar:
        st.title("📝 Smart ATS")
        st.subheader("Upload Your Documents")
        
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf", help="Please upload your resume in PDF format")
        jd = st.text_area("Job Description", height=200)
        github_username = st.text_input("GitHub Username (Optional)")
        
        submit = st.button("Analyze")

    # Main content area
    if not submit:
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

    if not uploaded_file or not jd:
        st.error("Please upload your resume and provide the job description.")
        return

    with st.spinner("Analyzing your resume..."):
        text = input_pdf_text(uploaded_file)
        github_data = None
        
        if github_username:
            # Workflow 2: Include GitHub analysis
            try:
                with st.spinner("Fetching GitHub data..."):
                    github_fetcher = GithubRepoFetcher(github_username)
                    github_data = github_fetcher.fetch_repo_info()
                    if not github_data:
                        st.warning(f"No public repositories found for user {github_username}")
                        response = get_gemini_response(
                            ats_prompt.format(
                                text=text,
                                jd=jd
                            )
                        )
                    else:
                        response = get_gemini_response(
                            github_analysis_prompt.format(
                                text=text,
                                jd=jd,
                                github_data=json.dumps(github_data)
                            )
                        )
            except Exception as e:
                st.error(f"Error fetching GitHub data: {str(e)}")
                return
        else:
            # Workflow 1: Basic ATS analysis
            response = get_gemini_response(
                ats_prompt.format(
                    text=text,
                    jd=jd
                )
            )
        
        try:
            # Clean the response string
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:-3]
            
            response_dict = json.loads(response)
            display_results(response_dict, github_data, bool(github_username))
            
        except json.JSONDecodeError as e:
            st.error("Error parsing the response. Please try again.")
            with st.expander("Show detailed error"):
                st.code(response)
                st.text(str(e))

if __name__ == "__main__":
    main()