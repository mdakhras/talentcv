import { useState, useRef, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import type { ChatMessage, AskRequest } from '../types';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';

interface ChatPanelProps {
  pendingQuestion?: string;
  onQuestionProcessed?: () => void;
}

export default function ChatPanel({ pendingQuestion, onQuestionProcessed }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'assistant',
      content: "Hello! I'm here to help you learn about Mohammed's professional background. You can browse the CV sections on the left and click on suggested questions, or ask me anything directly.",
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();

  const askMutation = useMutation({
    mutationFn: (request: AskRequest) => api.askQuestion(request),
    onSuccess: (response, variables) => {
      const assistantMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        citations: response.citations,
      };
      setMessages(prev => [...prev, assistantMessage]);
      scrollToBottom();
    },
    onError: (error) => {
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      scrollToBottom();
    }
  });

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const question = inputValue.trim();
    if (!question) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    
    askMutation.mutate({ question });
    scrollToBottom();
  };

  const handleQuestionClick = (question: string, section?: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    askMutation.mutate({ question, section });
    scrollToBottom();
  };

  useEffect(() => {
    if (pendingQuestion) {
      handleQuestionClick(pendingQuestion);
      onQuestionProcessed?.();
    }
  }, [pendingQuestion]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatTime = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit', 
      hour12: true 
    });
  };

  return (
    <Card className="flex flex-col h-full">
      <CardContent className="p-0 flex flex-col h-full">
        {/* Chat Header */}
        <div className="border-b border-border p-4">
          <h3 className="text-lg font-semibold text-card-foreground">Ask about the CV</h3>
          <p className="text-sm text-muted-foreground">Ask questions about any section or search freely</p>
        </div>

        {/* Chat Messages */}
        <div 
          ref={chatContainerRef}
          className="flex-1 overflow-y-auto chat-scroll p-4 space-y-4"
          data-testid="chat-messages-container"
        >
          {messages.map((message) => (
            <div 
              key={message.id} 
              className={`flex space-x-3 ${message.type === 'user' ? 'justify-end' : ''}`}
              data-testid={`message-${message.type}-${message.id}`}
            >
              {message.type === 'assistant' && (
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                  <i className="fas fa-robot text-primary-foreground text-sm"></i>
                </div>
              )}
              
              <div className="flex-1 flex justify-end">
                <div className={`rounded-lg px-4 py-3 max-w-md ${
                  message.type === 'user' 
                    ? 'bg-primary text-primary-foreground' 
                    : 'bg-muted text-muted-foreground'
                }`}>
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  
                  {message.citations && message.citations.length > 0 && (
                    <div className="border-t border-border pt-2 mt-3">
                      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Citations:</p>
                      <div className="flex flex-wrap gap-1">
                        {message.citations.map((citation, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="text-xs"
                            data-testid={`citation-${citation.section}-${index}`}
                          >
                            <i className="fas fa-link text-xs mr-1"></i>
                            {citation.section}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {message.type === 'user' && (
                <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                  <i className="fas fa-user text-secondary-foreground text-sm"></i>
                </div>
              )}
            </div>
          ))}

          {/* Loading State */}
          {askMutation.isPending && (
            <div className="flex space-x-3" data-testid="loading-message">
              <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                <i className="fas fa-robot text-primary-foreground text-sm"></i>
              </div>
              <div className="flex-1">
                <div className="bg-muted rounded-lg px-4 py-3 max-w-xs">
                  <div className="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Chat Input */}
        <div className="border-t border-border p-4">
          <form onSubmit={handleSubmit} className="flex space-x-3" data-testid="chat-input-form">
            <Input
              type="text"
              placeholder="Ask a question about the CV..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="flex-1"
              disabled={askMutation.isPending}
              data-testid="input-chat-message"
            />
            <Button
              type="submit"
              disabled={askMutation.isPending || !inputValue.trim()}
              data-testid="button-send-message"
            >
              <i className="fas fa-paper-plane text-sm"></i>
            </Button>
          </form>
          
          <div className="mt-2 text-xs text-muted-foreground">
            Ask about experience, skills, certifications, or anything else in the CV
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
