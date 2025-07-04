from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()

researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on job posting to help job applicants",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in navigating and extracting critical "
        "information from job postings is unmatched. Your skills help pinpoint the necessary "
        "qualifications and skills sought by employers, forming the foundation for effective "
        "application tailoring. Your Skills are to pinpoint the necessary qualifications and skills "
        "sought by employers, For that Job Posting."
    )
)
