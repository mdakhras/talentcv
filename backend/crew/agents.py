
try:
    from crewai import Agent
    # Try to import LLM - handle different CrewAI versions
    try:
        from crewai.llm import LLM
        CREWAI_LLM_AVAILABLE = True
    except ImportError:
        try:
            from crewai import LLM
            CREWAI_LLM_AVAILABLE = True
        except ImportError:
            try:
                from crewai.utilities.token_counter_callback import LLM
                CREWAI_LLM_AVAILABLE = True
            except ImportError:
                CREWAI_LLM_AVAILABLE = False
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    CREWAI_LLM_AVAILABLE = False

from crew.tools import cv_search, cv_sections, cv_content, set_retriever
from retriever import CVRetriever
import os
from dotenv import load_dotenv

load_dotenv()

def create_agents(retriever: CVRetriever):
    """Create CrewAI agents for CV question answering."""
    
    # Set the global retriever for tools
    set_retriever(retriever)
    
    if not CREWAI_AVAILABLE:
        print("CrewAI not available, using simple agents")
        return create_simple_agents(retriever)
    
    try:
        # Try to use Azure OpenAI if available and LLM class is available
        llm = None
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
        deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-35-turbo')
        
        # LLM settings
        llm_settings = {
            "temperature": 0,
            "max_tokens": 4000,
            "timeout_seconds": 120
        }
        
        if CREWAI_LLM_AVAILABLE and api_key and azure_endpoint:
            try:
                llm = LLM(
                    model=f"azure/{deployment_name}",
                    api_key=api_key,
                    base_url=azure_endpoint,
                    api_version=api_version,
                    temperature=llm_settings.get("temperature", 0),
                    max_tokens=llm_settings.get("max_tokens", 4000),
                    timeout=llm_settings.get("timeout_seconds", 120)
                )
                print(f"Azure LLM initialized successfully with deployment: {deployment_name}")
            except Exception as e:
                print(f"Azure LLM initialization failed: {e}")
                llm = None
        
        # If LLM initialization failed, use simple agents
        if not llm:
            print("Using simple agents due to LLM initialization issues")
            return create_simple_agents(retriever)
            
    except Exception as e:
        print(f"LLM initialization failed: {e}")
        # Fallback to simple agent approach
        return create_simple_agents(retriever)
    
    try:
        # CV Research Specialist
        if llm:
            cv_researcher = Agent(
                role='CV Research Specialist',
                goal='Find and extract relevant information from Mohammed Alakhras\'s CV to answer user questions accurately',
                backstory='''You are an expert at analyzing CVs and finding relevant information. 
                You have access to Mohammed Alakhras's complete CV and can search through all sections including 
                Experience, Skills, Certifications, Education, and more. Your job is to find the most relevant 
                information to answer user questions using the available CV search tools.''',
                tools=[cv_search, cv_sections, cv_content],
                llm=llm,
                verbose=True,
                allow_delegation=False
            )
            
            # CV Content Analyst
            cv_analyst = Agent(
                role='CV Content Analyst', 
                goal='Analyze and synthesize CV information to provide comprehensive and accurate answers',
                backstory='''You are a professional CV analyst who specializes in presenting candidate information 
                in a clear, comprehensive manner. You take the research findings and create well-structured, 
                accurate responses that highlight relevant qualifications, experience, and skills from Mohammed Alakhras's CV.''',
                tools=[cv_search, cv_content],
                llm=llm,
                verbose=True,
                allow_delegation=False
            )
        else:
            # Create agents without LLM for compatibility
            cv_researcher = Agent(
                role='CV Research Specialist',
                goal='Find and extract relevant information from Mohammed Alakhras\'s CV to answer user questions accurately',
                backstory='''You are an expert at analyzing CVs and finding relevant information. 
                You have access to Mohammed Alakhras's complete CV and can search through all sections including 
                Experience, Skills, Certifications, Education, and more. Your job is to find the most relevant 
                information to answer user questions using the available CV search tools.''',
                tools=[cv_search, cv_sections, cv_content],
                verbose=True,
                allow_delegation=False
            )
            
            # CV Content Analyst
            cv_analyst = Agent(
                role='CV Content Analyst', 
                goal='Analyze and synthesize CV information to provide comprehensive and accurate answers',
                backstory='''You are a professional CV analyst who specializes in presenting candidate information 
                in a clear, comprehensive manner. You take the research findings and create well-structured, 
                accurate responses that highlight relevant qualifications, experience, and skills from Mohammed Alakhras's CV.''',
                tools=[cv_search, cv_content],
                verbose=True,
                allow_delegation=False
            )
        
        print("CrewAI agents initialized successfully")
        
        return {
            'researcher': cv_researcher,
            'analyst': cv_analyst
        }
        
    except Exception as e:
        print(f"CrewAI agent creation failed: {e}")
        return create_simple_agents(retriever)

def create_simple_agents(retriever: CVRetriever):
    """Fallback simple agent system for CV question answering without crewai dependency."""
    
    class SimpleAgent:
        def __init__(self, role, goal, backstory, retriever):
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.retriever = retriever
        
        def process_query(self, question, section=None):
            """Process a query using the retriever."""
            try:
                context = self.retriever.get_context_for_query(question, section)
                if not context or context.strip() == "No relevant information found in the CV.":
                    return f"I couldn't find specific information about '{question}' in the CV."
                return context
            except Exception as e:
                return f"Error processing query: {str(e)}"
    
    cv_researcher = SimpleAgent(
        role='CV Research Specialist',
        goal='Find and extract relevant information from Mohammed Alakhras\'s CV to answer user questions accurately',
        backstory='''You are an expert at analyzing CVs and finding relevant information. 
        You have access to Mohammed Alakhras's complete CV and can search through all sections including 
        Experience, Skills, Certifications, Education, and more. Your job is to find the most relevant 
        information to answer user questions.''',
        retriever=retriever
    )
    
    cv_analyst = SimpleAgent(
        role='CV Content Analyst',
        goal='Analyze and synthesize CV information to provide comprehensive and accurate answers',
        backstory='''You are a professional CV analyst who specializes in presenting candidate information 
        in a clear, comprehensive manner. You take the research findings and create well-structured, 
        accurate responses that highlight relevant qualifications, experience, and skills.''',
        retriever=retriever
    )
    
    print("Simple CV agents initialized successfully (fallback mode)")
    
    return {
        'researcher': cv_researcher,
        'analyst': cv_analyst
    }
