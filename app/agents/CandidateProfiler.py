from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool, FileReadTool, MDXSearchTool

scrape_tool = ScrapeWebsiteTool()
search_tool = SerperDevTool()
read_resume = FileReadTool(file_path='./fake_resume.md')  # Replace with actual resume path as needed
semantic_search_resume = MDXSearchTool(mdx='./fake_resume.md')  # Replace as needed

# profiler = Agent(
#     role="Personal Profiler for Engineers",
#     goal="Do incredible research on job applicants to help them stand out in the job market",
#     tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
#     verbose=True,
#     backstory=(
#         "Equipped with analytical prowess, you dissect and synthesize information "
#         "from diverse sources to craft comprehensive personal and professional profiles, "
#         "laying the groundwork for personalized resume enhancements."
#     )
# )
profiler_agent = Agent(
    role="Candidate Profiler",
    goal="Create detailed candidate profiles based on job requirements and company culture",
    backstory="""You are a skilled profiler who analyzes job requirements and company information 
    to create comprehensive candidate profiles. You build upon research findings to understand 
    what makes an ideal candidate.""",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    memory=True,  # Access shared memory from JobResearcher
    allow_delegation=True,  # Can ask JobResearcher for clarification
    verbose=True
)