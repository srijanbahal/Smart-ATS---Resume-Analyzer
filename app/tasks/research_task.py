from crewai import Task
from app.agents.JobResearcher import researcher


research_task = Task(
    description="""Research the job position and company comprehensively:
    
    Job Details to Research:
    - Job title, responsibilities, and requirements
    - Required technical skills and experience level
    - Preferred qualifications and nice-to-haves
    - Salary range and benefits (if available)
    
    Company Research:
    - Company mission, values, and culture
    - Recent news, achievements, and challenges
    - Company size, industry, and market position
    - Technology stack and tools used
    - Leadership team and key personnel
    - Interview process and company reviews
    
    Industry Context:
    - Current industry trends and challenges
    - Competitive landscape
    - Skills in high demand
    
    Provide a comprehensive research report that will serve as the foundation 
    for all subsequent team analysis.""",
    expected_output="""Detailed research report containing:
    1. Complete job analysis with requirements breakdown
    2. Comprehensive company profile and culture analysis  
    3. Industry context and trends
    4. Key insights for candidate positioning""",
    agent=job_researcher
)
