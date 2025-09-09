from typing import Optional, Dict, Any
from retriever import CVRetriever

# Global retriever instance
retriever_instance = None

def set_retriever(retriever: CVRetriever):
    """Set the global retriever instance."""
    global retriever_instance
    retriever_instance = retriever

class SimpleTool:
    """Simple tool wrapper for CrewAI compatibility."""
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self.func = func
    
    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def cv_search_tool(query: str, section: Optional[str] = None) -> str:
    """
    Search through Mohammed Alakhras's CV to find relevant information.
    This tool can search across all sections or focus on a specific section like Experience, Skills, etc.
    Use this tool to retrieve factual information from the CV to answer user questions.
    
    Args:
        query: The search query to find relevant information in the CV
        section: Optional specific section to search in (e.g., 'Experience', 'Skills')
    
    Returns:
        Relevant context from the CV
    """
    try:
        if not retriever_instance:
            return "CV retriever not initialized"
        
        # Get relevant context using the retriever
        context = retriever_instance.get_context_for_query(query, section)
        
        if not context or context.strip() == "No relevant information found in the CV.":
            return f"No relevant information found in the CV for query: '{query}'"
        
        # Format the response with section information
        relevant_chunks = retriever_instance.search(query, section, top_k=5)
        sections_found = set()
        
        for chunk in relevant_chunks:
            sections_found.add(chunk['section'])
        
        response = f"Found relevant information in sections: {', '.join(sections_found)}\n\n"
        response += context
        
        return response
        
    except Exception as e:
        return f"Error searching CV: {str(e)}"

def cv_sections_tool() -> str:
    """
    Get a list of all available sections in Mohammed Alakhras's CV.
    Use this tool to understand what sections are available for more targeted searches.
    
    Returns:
        List of all available CV sections
    """
    try:
        if not retriever_instance:
            return "CV retriever not initialized"
        
        sections = retriever_instance.get_all_sections()
        return f"Available CV sections: {', '.join(sections)}"
    except Exception as e:
        return f"Error getting CV sections: {str(e)}"

def cv_content_tool(section: str) -> str:
    """
    Get the complete content of a specific section from Mohammed Alakhras's CV.
    Use this when you need comprehensive information from a particular section.
    
    Args:
        section: The section name to retrieve
        
    Returns:
        Complete content of the specified section
    """
    try:
        if not retriever_instance:
            return "CV retriever not initialized"
        
        content = retriever_instance.get_section_content(section)
        
        if not content:
            available_sections = retriever_instance.get_all_sections()
            return f"Section '{section}' not found. Available sections: {', '.join(available_sections)}"
        
        return f"## {section}\n\n{content}"
        
    except Exception as e:
        return f"Error retrieving section content: {str(e)}"

# Create tool objects for CrewAI
cv_search = SimpleTool(
    name="CV Search Tool",
    description="Search through Mohammed Alakhras's CV to find relevant information. This tool can search across all sections or focus on a specific section like Experience, Skills, etc. Use this tool to retrieve factual information from the CV to answer user questions.",
    func=cv_search_tool
)

cv_sections = SimpleTool(
    name="CV Section List Tool", 
    description="Get a list of all available sections in Mohammed Alakhras's CV. Use this tool to understand what sections are available for more targeted searches.",
    func=cv_sections_tool
)

cv_content = SimpleTool(
    name="CV Section Content Tool",
    description="Get the complete content of a specific section from Mohammed Alakhras's CV. Use this when you need comprehensive information from a particular section.",
    func=cv_content_tool
)
