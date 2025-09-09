from crewai import Task
from typing import Dict, Any

def create_tasks(agents: Dict, user_question: str, section: str = None) -> Dict:
    """Create CrewAI tasks for processing a user question about the CV."""
    
    # Task 1: Route the query to understand intent and scope
    route_task = Task(
        description=f"""Analyze this user question about Mohammed Alakhras's CV: "{user_question}"
        
        Your job is to:
        1. Identify what the user is asking about (experience, skills, education, etc.)
        2. Determine which CV sections would be most relevant
        3. Suggest the best search strategy
        
        {f"The user specified they want to focus on the '{section}' section." if section else ""}
        
        Provide a brief analysis of the query and recommended sections to search.""",
        agent=agents["router"],
        expected_output="A brief analysis of the user's question and the most relevant CV sections to search."
    )
    
    # Task 2: Retrieve relevant information from the CV
    retrieve_task = Task(
        description=f"""Based on the routing analysis, search Mohammed Alakhras's CV to find information relevant to: "{user_question}"
        
        Your job is to:
        1. Search the CV using the most appropriate queries
        2. Gather all relevant information from the CV
        3. Ensure you only use factual information from the CV
        4. Note which sections the information comes from
        
        {f"Focus your search on the '{section}' section as requested by the user." if section else ""}
        
        If the CV doesn't contain information to answer the question, clearly state that.
        Provide the raw factual information you found with section references.""",
        agent=agents["rag"],
        expected_output="Relevant factual information from the CV with clear section references, or a statement that the information is not available.",
        context=[route_task]
    )
    
    # Task 3: Refine the response for professional presentation
    refine_task = Task(
        description=f"""Create a professional, well-structured response to the user's question: "{user_question}"
        
        Using the information retrieved from Mohammed Alakhras's CV, create a response that:
        1. Directly answers the user's question
        2. Is well-organized and easy to read
        3. Uses bullet points when appropriate for lists
        4. Maintains a professional but conversational tone
        5. Includes clear citations showing which CV sections were used
        6. If information wasn't found, politely explains this and suggests related sections
        
        Format your final response as:
        - Main answer to the question
        - Citations: List the CV sections that were referenced
        
        Remember: Only use information that was actually found in the CV. Never make up or assume information.""",
        agent=agents["refiner"],
        expected_output="A professional, well-formatted response with clear citations to CV sections.",
        context=[route_task, retrieve_task]
    )
    
    return {
        "route": route_task,
        "retrieve": retrieve_task,
        "refine": refine_task
    }
