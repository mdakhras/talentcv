export interface CVSection {
  title: string;
  content: string;
  excerpt: string;
  icon: string;
}

export interface SuggestedQuestion {
  question: string;
  section: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: Citation[];
}

export interface Citation {
  section: string;
  subsection?: string;
}

export interface AskRequest {
  question: string;
  section?: string;
}

export interface AskResponse {
  answer: string;
  citations: Citation[];
  sources: string[];
}
