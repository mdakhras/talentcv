
from crewai import Agent
from crew.tools import cv_search, cv_sections, cv_content, set_retriever
from retriever import CVRetriever
import os
from dotenv import load_dotenv

load_dotenv()

def create_agents(retriever: CVRetriever):
    """Create CrewAI agents for CV question answering."""
    
    # Set the retriever for tools
    set_retriever(retriever)
    
    # Check if Azure OpenAI credentials are available
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    # Configure LLM based on available credentials
    llm_config = None
    if api_key and endpoint:
        try:
            from langchain_openai import AzureChatOpenAI
            llm_config = AzureChatOpenAI(
                azure_endpoint=endpoint,
                azure_deployment=os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT', 'gpt-4o-mini'),
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview'),
                api_key=api_key,
                temperature=0.1,
                max_tokens=1000
            )
            print("Azure OpenAI LLM initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI LLM: {e}")
            print("Will use retriever-only mode")
            llm_config = None
    else:
        print("Azure OpenAI credentials not found, using retriever-only mode")
    
    # Create agents
    cv_researcher = Agent(
        role='CV Research Specialist',
        goal='Find and extract relevant information from Mohammed Alakhras\'s CV to answer user questions accurately',
        backstory='''You are an expert at analyzing CVs and finding relevant information. 
        You have access to Mohammed Alakhras's complete CV and can search through all sections including 
        Experience, Skills, Certifications, Education, and more. Your job is to find the most relevant 
        information to answer user questions.''',
        tools=[cv_search, cv_sections, cv_content],
        llm=llm_config,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
    
    cv_analyst = Agent(
        role='CV Content Analyst',
        goal='Analyze and synthesize CV information to provide comprehensive and accurate answers',
        backstory='''You are a professional CV analyst who specializes in presenting candidate information 
        in a clear, comprehensive manner. You take the research findings and create well-structured, 
        accurate responses that highlight relevant qualifications, experience, and skills.''',
        tools=[cv_search, cv_content],
        llm=llm_config,
        verbose=True,
        allow_delegation=False,
        max_iter=2
    )
    
    return {
        'researcher': cv_researcher,
        'analyst': cv_analyst
    }
