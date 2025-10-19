import re
import markdown
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple

import markdown
from bs4 import BeautifulSoup
from typing import Dict, List

class CVLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = ""
        self.sections = {}
        
    def load_content(self) -> str:
        """Load the markdown content from file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
            return self.content
        except FileNotFoundError:
            raise FileNotFoundError(f"CV file not found at {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading CV file: {str(e)}")
    
    def parse_sections(self) -> Dict[str, Dict]:
        """Parse the markdown content into structured sections."""
        if not self.content:
            self.load_content()
        
        # Convert markdown to HTML for easier parsing
        html = markdown.markdown(self.content)
        soup = BeautifulSoup(html, 'html.parser')
        
        sections = {}
        current_section = None
        current_content = []
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'li']):
            if element.name in ['h1', 'h2']:
                # Save previous section if exists
                if current_section and current_content:
                    sections[current_section] = {
                        'title': current_section,
                        'content': '\n'.join(current_content),
                        'level': 1 if element.name == 'h1' else 2
                    }
                
                # Start new section
                current_section = element.get_text().strip()
                current_content = []
            else:
                # Add content to current section
                if current_section:
                    current_content.append(element.get_text().strip())
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = {
                'title': current_section,
                'content': '\n'.join(current_content),
                'level': 2
            }
        
        self.sections = sections
        return sections
    
    def get_structured_sections(self):
        """Get structured sections with title, content, and excerpt for API response."""
        if not self.sections:
            self.parse_sections()
        
        structured_sections = []
        for title, data in self.sections.items():
            content = data.get('content', '')
            # Create excerpt (first 150 characters)
            excerpt = content[:150] + '...' if len(content) > 150 else content
            
            structured_sections.append({
                'title': title,
                'content': content,
                'excerpt': excerpt,
                'icon': self._get_section_icon(title)
            })
        
        return structured_sections
    
    def _get_section_icon(self, section_title: str) -> str:
        """Get Font Awesome icon class for a section."""
        icons = {
            'Summary': 'fas fa-user-circle',
            'Experience': 'fas fa-briefcase',
            'Skills': 'fas fa-code',
            'Certificates': 'fas fa-certificate',
            'Languages': 'fas fa-globe',
            'Memberships': 'fas fa-users',
            'References': 'fas fa-address-book',
        }
        return icons.get(section_title, 'fas fa-file-alt')
    
    def get_chunks_for_embedding(self) -> List[Dict]:
        """Create chunks of content for embedding and retrieval."""
        if not self.sections:
            self.parse_sections()
        
        chunks = []
        for title, data in self.sections.items():
            content = data.get('content', '')
            
            # Split content into smaller chunks (by paragraphs or sentences)
            paragraphs = content.split('\n\n')
            
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    chunks.append({
                        'section': title,
                        'content': paragraph.strip(),
                        'chunk_id': f"{title}_{i}"
                    })
        
        return chunks
                
                # Start new section
                current_section = element.get_text().strip()
                current_content = []
                
            elif current_section:
                # Add content to current section
                text = element.get_text().strip()
                if text:
                    current_content.append(text)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = {
                'title': current_section,
                'content': '\n'.join(current_content),
                'level': 2
            }
        
        self.sections = sections
        return sections
    
    def get_section_excerpt(self, section_content: str, max_length: int = 150) -> str:
        """Generate a short excerpt from section content."""
        if len(section_content) <= max_length:
            return section_content
        
        # Find a good break point (end of sentence or word)
        excerpt = section_content[:max_length]
        last_period = excerpt.rfind('.')
        last_space = excerpt.rfind(' ')
        
        if last_period > max_length * 0.7:
            return excerpt[:last_period + 1]
        elif last_space > max_length * 0.7:
            return excerpt[:last_space] + "..."
        else:
            return excerpt + "..."
    
    def get_chunks_for_embedding(self, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """Break content into chunks suitable for embedding."""
        if not self.sections:
            self.parse_sections()
        
        chunks = []
        chunk_id = 0
        
        for section_name, section_data in self.sections.items():
            content = section_data['content']
            
            # Split content into sentences
            sentences = re.split(r'[.!?]+', content)
            
            current_chunk = ""
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # Check if adding this sentence would exceed chunk size
                test_chunk = current_chunk + " " + sentence if current_chunk else sentence
                
                if len(test_chunk) > chunk_size and current_chunk:
                    # Save current chunk
                    chunks.append({
                        'id': chunk_id,
                        'content': current_chunk.strip(),
                        'section': section_name,
                        'metadata': {
                            'section_title': section_name,
                            'level': section_data['level']
                        }
                    })
                    chunk_id += 1
                    
                    # Start new chunk with overlap
                    overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = test_chunk
            
            # Add the last chunk for this section
            if current_chunk.strip():
                chunks.append({
                    'id': chunk_id,
                    'content': current_chunk.strip(),
                    'section': section_name,
                    'metadata': {
                        'section_title': section_name,
                        'level': section_data['level']
                    }
                })
                chunk_id += 1
        
        return chunks
    
    def get_structured_sections(self) -> List[Dict]:
        """Get sections in a format suitable for the API."""
        if not self.sections:
            self.parse_sections()
        
        structured = []
        for section_name, section_data in self.sections.items():
            if section_name == "Mohammed Alakhras":  # Skip the name heading
                continue
                
            structured.append({
                'title': section_name,
                'content': section_data['content'],
                'excerpt': self.get_section_excerpt(section_data['content']),
                'icon': self._get_section_icon(section_name)
            })
        
        return structured
    
    def _get_section_icon(self, section_name: str) -> str:
        """Get appropriate icon for section."""
        icon_mapping = {
            'Summary': 'fas fa-user-circle',
            'Experience': 'fas fa-briefcase',
            'Skills': 'fas fa-code',
            'Certificates': 'fas fa-certificate',
            'Languages': 'fas fa-globe',
            'Memberships': 'fas fa-users',
            'References': 'fas fa-address-book'
        }
        return icon_mapping.get(section_name, 'fas fa-file-alt')
