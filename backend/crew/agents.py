from crewai import Agent
from crew.tools import cv_search, cv_sections, cv_content, set_retriever
from retriever import CVRetriever
import os
from dotenv import load_dotenv

load_dotenv()

def create_agents(retriever: CVRetriever):
    """Create CrewAI agents for the CV chatbot."""
    
    # Set the global retriever instance for tools
    set_retriever(retriever)
    
    # Common LLM configuration for Azure OpenAI
    llm_config = {
        "model": f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o-mini')}",
        "base_url": os.getenv('AZURE_OPENAI_ENDPOINT'),
        "api_key": os.getenv('AZURE_OPENAI_API_KEY'),
        "api_version": os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
    }
    
    # Router Agent - Classifies user intent and determines search strategy
    router_agent = Agent(
        role="CV Query Router",
        goal="Analyze user questions about Mohammed Alakhras's CV and determine the best approach to find relevant information",
        backstory="""You are an intelligent query router that helps users navigate Mohammed Alakhras's professional CV. 
        Your job is to understand what the user is asking about and determine which sections of the CV are most relevant.
        You can identify questions about experience, skills, education, certifications, languages, and other professional information.""",
        tools=[cv_sections],
        llm=llm_config,
        verbose=True,
        allow_delegation=False
    )
    
    # RAG Agent - Retrieves and synthesizes information from CV
    rag_agent = Agent(
        role="CV Information Retriever",
        goal="Find and synthesize relevant information from Mohammed Alakhras's CV to answer user questions accurately",
        backstory="""You are an expert at searching through and understanding professional CVs. 
        You have access to Mohammed Alakhras's complete CV and can find specific information about his experience, skills, 
        education, certifications, and other professional details. You always ground your responses in the actual CV content 
        and never make up information. If information is not in the CV, you clearly state that.""",
        tools=[cv_search, cv_content],
        llm=llm_config,
        verbose=True,
        allow_delegation=False
    )
    
    # Refiner Agent - Ensures professional, concise responses with proper citations
    refiner_agent = Agent(
        role="Response Refiner",
        goal="Create professional, well-structured responses about Mohammed Alakhras's CV with proper citations",
        backstory="""You are a professional communication specialist who takes raw information about Mohammed Alakhras 
        and crafts it into clear, engaging, and professional responses. You ensure all information is accurate, 
        well-organized, and includes proper citations to the CV sections used. You maintain a professional tone 
        while being conversational and helpful.""",
        tools=[],
        llm=llm_config,
        verbose=True,
        allow_delegation=False
    )
    
    return {
        "router": router_agent,
        "rag": rag_agent,
        "refiner": refiner_agent
    }
