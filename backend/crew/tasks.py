
from crewai import Task

def create_tasks(agents, query: str):
    """Create tasks for the CV assistant crew."""
    
    cv_query_task = Task(
        description=f"""
        Answer the user's question about Mohammed Alakhras's CV: "{query}"
        
        Use the available tools to search through the CV and find relevant information.
        Provide a comprehensive, accurate, and helpful response based on the CV content.
        
        Guidelines:
        - Always base your answers on the actual CV content
        - Be specific and provide concrete details when available
        - If information is not found in the CV, clearly state that
        - Format your response in a clear, professional manner
        - Include relevant sections or context when helpful
        """,
        agent=agents['cv_assistant'],
        expected_output="A detailed, accurate response to the user's question based on Mohammed Alakhras's CV content"
    )
    
    return [cv_query_task]
