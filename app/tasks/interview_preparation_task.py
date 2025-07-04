from crewai import Task
from agents.interview_preparer import interview_preparer
from tasks.research_task import research_task
from tasks.profile_task import profile_task
from tasks.resume_strategy_task import resume_strategy_task

interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion points. Make sure to use these questions and talking points to help the candidate highlight the main points of the resume and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)
