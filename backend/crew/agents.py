
from retriever import CVRetriever
import os
from dotenv import load_dotenv

load_dotenv()

def create_agents(retriever: CVRetriever):
    """Create a simple agent system for CV question answering without crewai dependency."""
    
    # Simple agent class that doesn't depend on crewai
    class SimpleAgent:
        def __init__(self, role, goal, backstory, retriever):
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.retriever = retriever
            self.llm = None
        
        def process_query(self, question, section=None):
            """Process a query using the retriever."""
            try:
                context = self.retriever.get_context_for_query(question, section)
                if not context or context.strip() == "No relevant information found in the CV.":
                    return f"I couldn't find specific information about '{question}' in the CV."
                return context
            except Exception as e:
                return f"Error processing query: {str(e)}"
    
    # Create simple agents without crewai dependency
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
    
    print("Simple CV agents initialized successfully (retriever-only mode)")
    
    return {
        'researcher': cv_researcher,
        'analyst': cv_analyst
    }
