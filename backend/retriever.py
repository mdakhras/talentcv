import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional, Tuple
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class CVRetriever:
    def __init__(self, chunks: List[Dict]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.chunk_vectors = None
        self.openai_client = None
        self._setup_openai()
        self._build_index()
    
    def _setup_openai(self):
        """Setup Azure OpenAI client if credentials are available."""
        try:
            api_key = os.getenv('AZURE_OPENAI_API_KEY')
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
            
            if api_key and endpoint:
                self.openai_client = openai.AzureOpenAI(
                    api_key=api_key,
                    azure_endpoint=endpoint,
                    api_version=api_version
                )
                print("Azure OpenAI client initialized successfully")
            else:
                print("Azure OpenAI credentials not found, using TF-IDF fallback")
        except Exception as e:
            print(f"Failed to initialize Azure OpenAI client: {e}")
            print("Using TF-IDF fallback for retrieval")
    
    def _build_index(self):
        """Build the search index from chunks."""
        if not self.chunks:
            raise ValueError("No chunks provided for indexing")
        
        # Extract text content from chunks
        texts = [chunk['content'] for chunk in self.chunks]
        
        # Build TF-IDF vectors
        self.chunk_vectors = self.vectorizer.fit_transform(texts)
        print(f"Built search index with {len(texts)} chunks")
    
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get embedding from Azure OpenAI."""
        if not self.openai_client:
            return None
        
        try:
            deployment = os.getenv('AZURE_OPENAI_EMBED_DEPLOYMENT', 'text-embedding-3-large')
            response = self.openai_client.embeddings.create(
                model=deployment,
                input=text
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def _tfidf_search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Fallback search using TF-IDF similarity."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.chunk_vectors)[0]
        
        # Get top k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                results.append((self.chunks[idx], float(similarities[idx])))
        
        return results
    
    def search(self, query: str, section: Optional[str] = None, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant chunks based on query and optional section filter.
        
        Args:
            query: The search query
            section: Optional section to filter by
            top_k: Number of top results to return
        
        Returns:
            List of relevant chunks with metadata
        """
        try:
            # Filter chunks by section if specified
            search_chunks = self.chunks
            if section:
                search_chunks = [
                    chunk for chunk in self.chunks 
                    if chunk['section'].lower() == section.lower()
                ]
                if not search_chunks:
                    print(f"No chunks found for section: {section}")
                    search_chunks = self.chunks
            
            # Try Azure OpenAI embedding search first
            embedding = self._get_embedding(query)
            
            if embedding is not None and hasattr(self, 'chunk_embeddings'):
                # Use embedding-based search (if we had pre-computed embeddings)
                return self._embedding_search(query, embedding, search_chunks, top_k)
            else:
                # Fall back to TF-IDF search
                if section:
                    # Rebuild vectorizer for filtered chunks
                    texts = [chunk['content'] for chunk in search_chunks]
                    if texts:
                        temp_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
                        temp_vectors = temp_vectorizer.fit_transform(texts)
                        query_vector = temp_vectorizer.transform([query])
                        similarities = cosine_similarity(query_vector, temp_vectors)[0]
                        
                        top_indices = np.argsort(similarities)[::-1][:top_k]
                        results = []
                        for idx in top_indices:
                            if similarities[idx] > 0.1:
                                chunk = search_chunks[idx].copy()
                                chunk['similarity'] = float(similarities[idx])
                                results.append(chunk)
                        return results
                
                # Use global TF-IDF search
                results = self._tfidf_search(query, top_k)
                return [
                    {**chunk, 'similarity': score} 
                    for chunk, score in results
                ]
        
        except Exception as e:
            print(f"Error in search: {e}")
            # Return a fallback result
            return self.chunks[:top_k] if self.chunks else []
    
    def get_section_content(self, section: str) -> str:
        """Get all content for a specific section."""
        section_chunks = [
            chunk for chunk in self.chunks 
            if chunk['section'].lower() == section.lower()
        ]
        
        if not section_chunks:
            return ""
        
        # Combine all chunks for the section
        content = "\n\n".join([chunk['content'] for chunk in section_chunks])
        return content
    
    def get_all_sections(self) -> List[str]:
        """Get list of all available sections."""
        sections = set()
        for chunk in self.chunks:
            sections.add(chunk['section'])
        return sorted(list(sections))
    
    def get_context_for_query(self, query: str, section: Optional[str] = None, max_context_length: int = 2000) -> str:
        """
        Get relevant context for a query, formatted for LLM consumption.
        
        Args:
            query: The user's question
            section: Optional section to focus on
            max_context_length: Maximum length of context to return
        
        Returns:
            Formatted context string
        """
        relevant_chunks = self.search(query, section, top_k=10)
        
        if not relevant_chunks:
            return "No relevant information found in the CV."
        
        context_parts = []
        current_length = 0
        
        for chunk in relevant_chunks:
            section_header = f"\n## {chunk['section']}\n"
            chunk_text = chunk['content']
            
            # Check if adding this chunk would exceed max length
            addition_length = len(section_header) + len(chunk_text)
            if current_length + addition_length > max_context_length and context_parts:
                break
            
            context_parts.append(section_header + chunk_text)
            current_length += addition_length
        
        context = "".join(context_parts)
        
        if current_length >= max_context_length:
            context += "\n\n[Note: Additional relevant information may be available in the CV]"
        
        return context
