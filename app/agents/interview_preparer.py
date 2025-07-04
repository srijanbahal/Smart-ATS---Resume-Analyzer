from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileReadTool, MDXSearchTool

scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()
read_resume = FileReadTool(file_path='./fake_resume.md')  # Replace with actual resume path as needed
semantic_search_resume = MDXSearchTool(mdx='./fake_resume.md')  # Replace as needed

interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points based on the resume and job requirements",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, ensuring they can confidently address all aspects of the "
        "job they are applying for."
    )
)
