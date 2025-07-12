from crewai import Task
from app.agents.ResumeStrategist import resume_strategist
from tasks.research_task import research_task
from tasks.profile_task import profile_task

# resume_strategy_task = Task(
#     description=(
#         "Using the profile and job requirements obtained from previous tasks, tailor the resume to highlight the most relevant areas. "
#         "Employ tools to adjust and enhance the resume content. Make sure this is the best resume but don't make up any information. "
#         "Update every section, including the initial summary, work experience, skills, and education. All to better reflect the candidate's abilities and how it matches the job posting."
#     ),
#     expected_output=(
#         "An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job."
#     ),
#     output_file="tailored_resume.md",
#     context=[research_task, profile_task],
#     agent=resume_strategist
# )

resume_strategy_task = Task(
    description="""Create a targeted resume strategy based on all research and analysis:
    
    - Prioritize experiences that align with job requirements
    - Craft compelling bullet points using company language/values
    - Highlight technical skills that match the tech stack
    - Address any gaps or concerns identified in profiling
    - Suggest keywords and phrases for ATS optimization
    
    Create a comprehensive resume strategy that maximizes candidate appeal.""",
    expected_output="""Resume strategy guide including:
    1. Prioritized experience sections and bullet points
    2. Technical skills highlighting strategy
    3. Keywords and ATS optimization recommendations
    4. Gap addressing and positioning strategies""",
    agent=resume_strategist,
    context=[research_task, profiling_task, github_analysis_task]
)