from crewai import Task
from agents.resume_strategist import resume_strategist
from tasks.research_task import research_task
from tasks.profile_task import profile_task

resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from previous tasks, tailor the resume to highlight the most relevant areas. "
        "Employ tools to adjust and enhance the resume content. Make sure this is the best resume but don't make up any information. "
        "Update every section, including the initial summary, work experience, skills, and education. All to better reflect the candidate's abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)
