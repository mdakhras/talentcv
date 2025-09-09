# CV Chatbot

## Overview

This is an AI-powered CV chatbot application that provides an interactive interface for users to learn about Mohammed Alakhras's professional background. The system consists of a React frontend with a Flask backend that uses CrewAI agents and Azure OpenAI for intelligent question answering about CV content.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React with TypeScript using Vite as the build tool
- **UI Library**: Shadcn/ui components built on Radix UI primitives
- **Styling**: Tailwind CSS with custom design tokens and dark/light theme support
- **State Management**: TanStack Query for server state management
- **Routing**: Wouter for lightweight client-side routing
- **Component Structure**: Modular design with reusable UI components and separate page components

### Backend Architecture
- **Framework**: Flask (Python) serving as the API backend
- **AI Framework**: CrewAI for orchestrating AI agents that handle different aspects of CV querying
- **Agent Architecture**: 
  - Router Agent: Classifies user intent and determines search strategy
  - RAG Agent: Retrieves and synthesizes information from CV content
  - Refine Agent: Formats responses professionally
- **Document Processing**: Markdown parsing with BeautifulSoup for CV content extraction
- **Search Implementation**: TF-IDF vectorization with scikit-learn as fallback, Azure OpenAI embeddings when available

### Node.js Server Layer
- **Express.js**: Serves the frontend and proxies API requests to the Flask backend
- **Development Setup**: Automatic Flask process spawning during development
- **Vite Integration**: HMR support and development middleware
- **API Proxying**: Routes `/api/*` requests to Flask backend on port 8000

### Data Storage Solutions
- **Database**: PostgreSQL with Drizzle ORM configured for user management
- **CV Storage**: Markdown file (`backend/data/cv.md`) processed into structured sections
- **Session Management**: Express sessions with PostgreSQL store
- **In-Memory Search Index**: TF-IDF vectors stored in memory for fast retrieval

### Authentication and Authorization
- **User Schema**: Basic username/password authentication system with Drizzle
- **Session Storage**: PostgreSQL-based session store using connect-pg-simple
- **Memory Fallback**: In-memory user storage for development

## External Dependencies

### AI and Machine Learning
- **Azure OpenAI**: Primary LLM service for chat completions and embeddings
- **CrewAI**: Multi-agent framework for coordinating AI workflows
- **OpenAI SDK**: Official client library for Azure OpenAI integration
- **scikit-learn**: Fallback for TF-IDF vectorization and similarity calculations

### Database and Storage
- **PostgreSQL**: Primary database using Neon serverless
- **Drizzle ORM**: Type-safe database operations and migrations
- **connect-pg-simple**: PostgreSQL session store

### Frontend Libraries
- **Radix UI**: Unstyled accessible component primitives
- **TanStack Query**: Server state management and caching
- **Tailwind CSS**: Utility-first CSS framework
- **date-fns**: Date manipulation utilities
- **clsx/class-variance-authority**: Conditional class name utilities

### Development and Build Tools
- **Vite**: Fast frontend build tool and development server
- **TypeScript**: Type safety across the entire application
- **ESBuild**: Fast bundling for production builds
- **Replit Integration**: Runtime error modal and cartographer plugins