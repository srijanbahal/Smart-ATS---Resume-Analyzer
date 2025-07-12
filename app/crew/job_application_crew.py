from agents.InterviewPreparer import interview_preparer
from agents.CandidateProfiler import profiler_agent
from agents.GithubAnalyzer import github_analyzer
from agents.JobResearcher import job_researcher
from agents.ResumeStrategist import resume_strategist
from tasks.github_analyzer_task import github_analysis_task
from tasks.interview_preparation_task import interview_prep_task
from tasks.profile_task import profiling_task
from tasks.research_task import research_task
from tasks.resume_strategy_task import resume_strategy_task
from crewai import Crew, Process





job_application_crew = Crew(
    agents=[
        job_researcher,
        profiler_agent, 
        github_analyzer,
        resume_strategist,
        interview_preparer
    ],
    tasks=[
        research_task,
        profiling_task,
        github_analysis_task, 
        resume_strategy_task,
        interview_prep_task
    ],
    process=Process.sequential,  # Execute in order
    memory=True,  # Enable shared memory across all agents
    verbose=True
)