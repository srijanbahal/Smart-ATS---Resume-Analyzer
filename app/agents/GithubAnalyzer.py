from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileReadTool, MDXSearchTool, GithubSearchTool

overAllSearchWithinRepo = GithubSearchTool(
    config=config,
    gh_token=gh_token,  # Replace with your GitHub token
    content_types=["code", "issues", "pull_requests", "discussions"],
    
)

# codeSearchTool = GithubSearchTool(
#     config=config,
#     gh_token = gh_token,  # Replace with your GitHub token    
#     content_types=["code"],
# )


github_analyzer = Agent(
    role="GitHub Portfolio Analyst", 
    goal="Analyze GitHub profiles and repositories for job alignment",
    backstory="""You are a technical recruiter who specializes in evaluating GitHub profiles 
    and code repositories. You assess technical skills and project alignment based on job 
    requirements and company tech stack.""",
    tools=[scrape_tool],  # Add GitHub-specific tools as needed
    memory=True,  # Access research findings about tech requirements
    allow_delegation=True,  # Can ask for specific technical requirements
    verbose=True
)
