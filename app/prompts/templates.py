"""
Collection of prompt templates for the ATS system
"""

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
    "Profile Summary": "detailed summary with bullet points here (note : it will be in context of addressing user as you or your)",
    "ProjectMatch": "X%",
    "WorkExpMatch": "X%",
    "EduMatch": "X%"
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
    "ProjectMatch": "X%",
    "WorkExpMatch": "X%",
    "EduMatch": "X%",
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