from crewai import Task
from app.agents.CandidateProfiler import profiler

# profile_task = Task(
#     description=(
#         "Compile a detailed personal and professional profile using the GitHub ({github_url}) URLs, and personal write-up ({personal_writeup}). "
#         "Utilize tools to extract and synthesize information from these sources."
#     ),
#     expected_output=(
#         "A comprehensive profile document that includes skills, project experiences, contributions, interests, and communication style."
#     ),
#     agent=profiler,
#     async_execution=True
# )

profiling_task = Task(
    description="""Based on the job and company research, create an ideal candidate profile:
    
    - Analyze job requirements to identify must-have vs nice-to-have skills
    - Map company culture to personality traits and work style preferences
    - Identify key experience areas that would be most valuable
    - Determine optimal candidate positioning strategy
    - Highlight potential red flags or challenges to address
    
    Use the research findings to create a comprehensive ideal candidate profile.""",
    expected_output="""Ideal candidate profile including:
    1. Priority-ranked skills and qualifications
    2. Cultural fit requirements and personality traits
    3. Experience mapping and positioning strategy
    4. Potential challenges and mitigation approaches""",
    agent=profiler_agent,
    context=[research_task]  # Gets research output as context
)
