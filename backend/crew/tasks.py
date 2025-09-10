
from crewai import Task
import os

def create_tasks(agents, question: str, section: str = None):
    """Create CrewAI tasks for answering CV questions."""
    
    # Check if we have LLM capabilities
    has_llm = bool(os.getenv('AZURE_OPENAI_API_KEY') and os.getenv('AZURE_OPENAI_ENDPOINT'))
    
    if section:
        context_info = f"Focus specifically on the '{section}' section of the CV."
    else:
        context_info = "Search across all relevant sections of the CV."
    
    research_task = Task(
        description=f'''
        Research and find relevant information from Mohammed Alakhras's CV to answer this question: "{question}"
        
        {context_info}
        
        Instructions:
        1. Use the CV search tool to find relevant information
        2. If searching a specific section, use the CV content tool for comprehensive information
        3. Gather all relevant details that help answer the question
        4. Focus on factual information from the CV
        
        Return the relevant information found in the CV.
        ''',
        agent=agents['researcher'],
        expected_output="Relevant information from the CV that helps answer the user's question"
    )
    
    if has_llm:
        analysis_task = Task(
            description=f'''
            Based on the research findings, provide a comprehensive and accurate answer to: "{question}"
            
            Instructions:
            1. Synthesize the research findings into a clear, well-structured response
            2. Ensure all information is factually accurate and comes from the CV
            3. Organize the response logically and professionally
            4. Include specific details like dates, company names, technologies, etc. when relevant
            5. If no relevant information was found, clearly state that
            
            Provide a professional response that directly answers the user's question.
            ''',
            agent=agents['analyst'],
            context=[research_task],
            expected_output="A comprehensive, accurate answer to the user's question based on CV information"
        )
        
        return {
            'research': research_task,
            'analysis': analysis_task
        }
    else:
        # Fallback: just return research task when no LLM is available
        return {
            'research': research_task
        }
