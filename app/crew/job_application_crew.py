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