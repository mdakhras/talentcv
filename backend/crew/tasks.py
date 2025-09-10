
try:
    from crewai import Task
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
import os

def create_tasks(agents, question, section=None):
    """Create CrewAI tasks for CV question answering."""
    
    if not CREWAI_AVAILABLE:
        # Return simple task objects for fallback mode
        return create_simple_tasks(agents, question, section)
    
    try:
        # Research task
        research_task = Task(
            description=f"""
            Research and find relevant information from Mohammed Alakhras's CV to answer the following question:
            
            Question: {question}
            Section focus: {section if section else 'All sections'}
            
            Your goal is to:
            1. Use the CV search tools to find relevant information
            2. Look through appropriate sections of the CV
            3. Extract specific details that directly answer the question
            4. Gather comprehensive information to provide a complete answer
            
            Focus on finding factual information from the CV content.
            """,
            agent=agents['researcher'],
            expected_output="Relevant information and context from the CV that answers the question"
        )
        
        # Analysis task
        analysis_task = Task(
            description=f"""
            Based on the research findings, provide a comprehensive and well-structured answer to:
            
            Question: {question}
            
            Your goal is to:
            1. Analyze the research findings
            2. Create a clear, professional response
            3. Highlight relevant qualifications, experience, and skills
            4. Provide specific examples and details from the CV
            5. Ensure the answer is accurate and complete
            
            Format your response in a professional manner suitable for someone asking about Mohammed Alakhras's qualifications.
            """,
            agent=agents['analyst'],
            expected_output="A comprehensive, professional answer based on CV information with specific details and examples",
            context=[research_task]
        )
        
        return {
            'research': research_task,
            'analysis': analysis_task
        }
        
    except Exception as e:
        print(f"CrewAI task creation failed: {e}")
        return create_simple_tasks(agents, question, section)

def create_simple_tasks(agents, question, section=None):
    """Create simple task objects for fallback mode."""
    
    class SimpleTask:
        def __init__(self, description, agent, expected_output):
            self.description = description
            self.agent = agent
            self.expected_output = expected_output
        
        def execute(self):
            """Execute the task using the agent."""
            return self.agent.process_query(question, section)
    
    research_task = SimpleTask(
        description=f"Research information for: {question}",
        agent=agents['researcher'],
        expected_output="Relevant CV information"
    )
    
    analysis_task = SimpleTask(
        description=f"Analyze and format answer for: {question}",
        agent=agents['analyst'], 
        expected_output="Formatted professional answer"
    )
    
    return {
        'research': research_task,
        'analysis': analysis_task
    }
