from crewai import Task
from agents.GithubAnalyzer import GitHubAnalyzer

# GitHubAnalyzerTask = Task(
#     description=(
#         "Using the job description and role extracted earlier, perform semantic search "
#         "across the user's GitHub repositories to find the most relevant project(s) "
#         "aligned with the company's domain and required tech stack. "
#         "Summarize the top matching project and explain why it's a strong fit."
#     ),
#     agent=GitHubAnalyzer,
#     expected_output=(
#         "A Markdown summary of the most relevant GitHub project including: "
#         "- Repo name\n- Description\n- Why it matches the job\n- Tech stack used\n- GitHub link"
#     ),
# )

github_analysis_task = Task(
    description="""Analyze the candidate's GitHub profile against job requirements:
    
    - Review repositories for relevant technical skills
    - Assess code quality and project complexity
    - Identify projects that align with company's tech stack
    - Evaluate contribution patterns and collaboration skills
    - Suggest improvements or highlights for the application
    
    Base your analysis on the job requirements and ideal candidate profile.""",
    expected_output="""GitHub analysis report with:
    1. Technical skills assessment vs job requirements
    2. Relevant project highlights and recommendations
    3. Areas for improvement or additional showcasing
    4. Strategic recommendations for GitHub optimization""",
    agent=github_analyzer,
    context=[research_task, profiling_task]  # Uses both previous outputs
)
