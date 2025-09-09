import { apiRequest } from './queryClient';
import type { CVSection, SuggestedQuestion, AskRequest, AskResponse } from '../types';

const API_BASE = '/api';

export const api = {
  async getSections(): Promise<CVSection[]> {
    const response = await apiRequest('GET', `${API_BASE}/sections`);
    return response.json();
  },

  async getQuestions(section?: string): Promise<SuggestedQuestion[]> {
    const url = section 
      ? `${API_BASE}/questions?section=${encodeURIComponent(section)}`
      : `${API_BASE}/questions`;
    const response = await apiRequest('GET', url);
    return response.json();
  },

  async askQuestion(request: AskRequest): Promise<AskResponse> {
    const response = await apiRequest('POST', `${API_BASE}/ask`, request);
    return response.json();
  },

  async getHealth(): Promise<{ status: string }> {
    const response = await apiRequest('GET', `${API_BASE}/health`);
    return response.json();
  }
};
