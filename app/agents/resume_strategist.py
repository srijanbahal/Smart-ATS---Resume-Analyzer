from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileReadTool, MDXSearchTool

scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()
read_resume = FileReadTool(file_path='./fake_resume.md')  # Replace with actual resume path as needed
semantic_search_resume = MDXSearchTool(mdx='./fake_resume.md')  # Replace as needed

resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a resume stand out in the job market.",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they resonate perfectly with the job's requirements."
    )
)
