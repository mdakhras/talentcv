
import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from loader import CVLoader
from retriever import CVRetriever
from crew.agents import create_agents
from crew.tasks import create_tasks

# Check if CrewAI is available
try:
    from crewai import Crew
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, origins=[
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5000",  # Production
    "https://*.replit.dev",   # Replit domains
    "https://*.repl.co"       # Replit domains
])

# Global variables for CV data
cv_loader = None
retriever = None
agents = None

def initialize_cv_system():
    """Initialize the CV loading and retrieval system."""
    global cv_loader, retriever, agents
    
    try:
        # Load CV data
        cv_path = os.path.join(backend_dir, 'data', 'cv.md')
        logger.info(f"Loading CV from: {cv_path}")
        
        if not os.path.exists(cv_path):
            logger.error(f"CV file not found: {cv_path}")
            return False
        
        cv_loader = CVLoader(cv_path)
        cv_loader.load_content()
        
        # Parse sections and create chunks
        chunks = cv_loader.get_chunks_for_embedding()
        logger.info(f"Created {len(chunks)} chunks from CV")
        
        if not chunks:
            logger.error("No chunks created from CV")
            return False
        
        # Initialize retriever
        retriever = CVRetriever(chunks)
        logger.info("CV retriever initialized")
        
        # Create agents
        agents = create_agents(retriever)
        logger.info("CV agents created")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize CV system: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

# Suggested questions for each section
SECTION_QUESTIONS = {
    "Summary": [
        "Tell me about Mohammed's professional background",
        "What are his core competencies?",
        "What is his expertise in information management?"
    ],
    "Experience": [
        "What impact did you deliver at IOM?",
        "How did you apply DevOps practices?",
        "Tell me about your UNRWA experience",
        "What AI projects have you worked on?",
        "Describe your leadership experience"
    ],
    "Skills": [
        "What programming languages do you know?",
        "What are your cloud technology skills?",
        "Tell me about your DevOps expertise",
        "What AI and machine learning skills do you have?"
    ],
    "Certificates": [
        "What certifications do you have?",
        "Tell me about your AWS certification",
        "What professional certifications have you earned?"
    ],
    "Languages": [
        "What languages do you speak?",
        "What is your level in Spanish?",
        "Tell me about your communication skills"
    ],
    "Memberships": [
        "What professional organizations do you belong to?",
        "Tell me about your professional memberships"
    ],
    "References": [
        "Who can provide references for you?",
        "Tell me about your professional references"
    ]
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    status = "healthy" if retriever is not None else "initializing"
    return jsonify({"status": status})

@app.route('/api/sections', methods=['GET'])
def get_sections():
    """Get all CV sections with excerpts."""
    try:
        if not cv_loader:
            return jsonify({"error": "CV system not initialized"}), 500
        
        sections = cv_loader.get_structured_sections()
        return jsonify(sections)
        
    except Exception as e:
        logger.error(f"Error getting sections: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get suggested questions for a section or all sections."""
    try:
        section = request.args.get('section')
        
        if section:
            questions = SECTION_QUESTIONS.get(section, [])
            return jsonify([{"question": q, "section": section} for q in questions])
        else:
            # Return all questions
            all_questions = []
            for sec, questions in SECTION_QUESTIONS.items():
                all_questions.extend([{"question": q, "section": sec} for q in questions])
            return jsonify(all_questions)
            
    except Exception as e:
        logger.error(f"Error getting questions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Process a question using CrewAI agents."""
    try:
        if not retriever or not agents:
            return jsonify({"error": "CV system not initialized"}), 500
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Question is required"}), 400
        
        question = data['question'].strip()
        section = data.get('section')
        
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        logger.info(f"Processing question: {question} (section: {section})")
        
        # Try to use CrewAI if available
        if CREWAI_AVAILABLE and hasattr(agents['researcher'], 'tools'):
            try:
                # Create tasks
                tasks = create_tasks(agents, question, section)
                
                # Create crew
                crew = Crew(
                    agents=[agents['researcher'], agents['analyst']],
                    tasks=[tasks['research'], tasks['analysis']],
                    verbose=True
                )
                
                # Execute crew
                result = crew.kickoff()
                answer = str(result)
                
            except Exception as e:
                logger.error(f"CrewAI execution failed: {e}")
                # Fallback to simple agent processing
                researcher = agents['researcher']
                answer = researcher.process_query(question, section)
        else:
            # Use simple agent processing
            researcher = agents['researcher']
            answer = researcher.process_query(question, section)
        
        if not answer or "couldn't find specific information" in answer:
            answer = f"I couldn't find specific information about '{question}' in the CV. Please try a different question or check the available sections."
        else:
            answer = f"Based on the CV information:\n\n{answer}"
        
        # Generate citations
        citations = []
        relevant_chunks = retriever.search(question, section, top_k=3)
        seen_sections = set()
        
        for chunk in relevant_chunks:
            if chunk['section'] not in seen_sections:
                citations.append({"section": chunk['section']})
                seen_sections.add(chunk['section'])
        
        response = {
            "answer": answer,
            "citations": citations,
            "sources": [cite["section"] for cite in citations]
        }
        
        logger.info(f"Response generated with {len(citations)} citations")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({
            "error": "Failed to process question",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Initialize the CV system
    logger.info("Starting CV Chatbot backend...")
    
    if not initialize_cv_system():
        logger.error("Failed to initialize CV system. Exiting.")
        sys.exit(1)
    
    logger.info("CV system initialized successfully")
    
    # Start the Flask app on port 5001 to avoid conflicts with the frontend
    port = int(os.environ.get('FLASK_PORT', 5001))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
