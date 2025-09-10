from crewai import Agent
from crew.tools import cv_search, cv_sections, cv_content, set_retriever
from retriever import CVRetriever
import os
from dotenv import load_dotenv

load_dotenv()

def create_agents(retriever: CVRetriever):
    """Create and configure CrewAI agents."""
    # Set the retriever for tools
    set_retriever(retriever)

    cv_assistant = Agent(
        role='CV Assistant',
        goal='Help users understand and explore Mohammed Alakhras\'s professional background, skills, and experience through his CV',
        backstory="""You are a knowledgeable assistant specializing in Mohammed Alakhras's CV. 
        You have deep understanding of his professional background, technical skills, certifications, 
        and career journey. You can provide detailed insights about his experience, projects, 
        and qualifications to help users understand his capabilities and expertise.""",
        tools=[cv_search, cv_sections, cv_content],
        verbose=True,
        allow_delegation=False
    )

    return {'cv_assistant': cv_assistant}