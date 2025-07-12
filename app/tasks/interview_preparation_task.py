from crewai import Task
from agents.InterviewPreparer import interview_preparer
from tasks.research_task import research_task
from tasks.profile_task import profile_task
from tasks.resume_strategy_task import resume_strategy_task

# interview_preparation_task = Task(
#     description=(
#         "Create a set of potential interview questions and talking points based on the tailored resume and job requirements. "
#         "Utilize tools to generate relevant questions and discussion points. Make sure to use these questions and talking points to help the candidate highlight the main points of the resume and how it matches the job posting."
#     ),
#     expected_output=(
#         "A document containing key questions and talking points that the candidate should prepare for the initial interview."
#     ),
#     output_file="interview_materials.md",
#     context=[research_task, profile_task, resume_strategy_task],
#     agent=interview_preparer
# )

interview_prep_task = Task(
    description="""Prepare comprehensive interview materials based on all team analysis:
    
    - Create likely interview questions based on company research
    - Develop STAR method responses using candidate's background
    - Prepare technical questions related to the role
    - Create company-specific questions to ask interviewers
    - Develop strategies for addressing potential concerns
    - Prepare salary negotiation talking points
    
    Use all available research and analysis to create thorough interview prep.""",
    expected_output="""Complete interview preparation package:
    1. Anticipated interview questions with suggested responses
    2. Technical preparation areas and practice problems
    3. Company-specific questions to ask interviewers
    4. Concern addressing strategies and talking points
    5. Salary negotiation preparation and market data""",
    agent=interview_preparer,
    context=[research_task, profiling_task, github_analysis_task, resume_strategy_task]
)