
# CV Chatbot

## Overview

This is an AI-powered CV chatbot application that provides an interactive interface for users to learn about Mohammed Alakhras's professional background. The system consists of a React frontend with TypeScript, a Node.js/Express server layer, and a Flask backend that uses CrewAI agents and Azure OpenAI for intelligent question answering about CV content.

## Current Status

⚠️ **Note**: The application is currently experiencing an initialization issue with the Flask backend due to a missing `create_agents` function in the CrewAI setup. The frontend and Node.js server are working correctly.

## System Architecture

### Frontend
- **Framework**: React with TypeScript using Vite
- **UI Library**: Shadcn/ui components built on Radix UI
- **Styling**: Tailwind CSS with dark/light theme support
- **State Management**: TanStack Query for server state
- **Routing**: Wouter for client-side routing

### Backend Services
- **Node.js Server**: Express.js serving frontend and proxying API requests
- **Flask API**: Python backend with CrewAI agents for CV processing
- **AI Framework**: CrewAI for multi-agent CV querying (currently needs repair)
- **Document Processing**: Markdown parsing with CV content extraction
- **Search**: TF-IDF vectorization with scikit-learn, Azure OpenAI embeddings support

### Database & Storage
- **Database**: PostgreSQL with Drizzle ORM (configured but not actively used)
- **CV Data**: Stored in `backend/data/cv.md`
- **Session Management**: Express sessions with PostgreSQL store

## Features

- Interactive chat interface for CV questions
- Multi-agent AI system for intelligent responses
- Section-based CV content organization
- Suggested questions by CV section
- Citation support showing information sources
- Responsive design with dark/light themes

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- PostgreSQL database (optional, for user management)

## Environment Variables

Create a `.env` file in the `backend` directory:

```
# Azure OpenAI Configuration (optional)
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=your_chat_deployment
AZURE_OPENAI_EMBED_DEPLOYMENT=your_embedding_deployment

# Database Configuration (optional)
DATABASE_URL=your_postgresql_url
```

## Installation & Setup

### Automatic Setup (Recommended)
The application uses automatic dependency management. Simply click the "Run" button in Replit, which will:
1. Install Node.js dependencies via npm
2. Install Python dependencies via uv/pip
3. Start both the Node.js server and Flask backend

### Manual Setup
If you need to install dependencies manually:

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd backend
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
npm run dev
```

This starts:
- Node.js/Express server on port 5000
- Flask backend on port 8000 (automatically spawned)
- Vite development server with HMR

### Production Mode
```bash
npm run build
npm start
```

## Project Structure

```
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Page components
│   │   ├── lib/            # Utilities and API client
│   │   └── types/          # TypeScript definitions
├── server/                 # Node.js/Express server
│   ├── index.ts           # Main server file
│   ├── routes.ts          # API route definitions
│   └── vite.ts            # Vite integration
├── backend/               # Python Flask backend
│   ├── crew/              # CrewAI agents and tools
│   ├── data/              # CV data files
│   ├── app.py             # Flask application
│   ├── retriever.py       # CV search and retrieval
│   └── loader.py          # CV content processing
└── shared/                # Shared TypeScript schemas
```

## Known Issues

1. **Flask Backend Initialization**: The `create_agents` function is missing from the CrewAI setup, causing the backend to fail during startup.
2. **Azure OpenAI Fallback**: When Azure OpenAI credentials are not provided, the system falls back to TF-IDF search, which works but with reduced accuracy.

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/sections` - Get available CV sections
- `GET /api/questions` - Get suggested questions
- `POST /api/ask` - Ask a question about the CV

## Technologies Used

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Shadcn/ui component library
- TanStack Query for state management
- Wouter for routing

### Backend
- Flask (Python) for API
- CrewAI for multi-agent AI workflows
- Azure OpenAI for LLM capabilities
- scikit-learn for text processing
- BeautifulSoup for HTML parsing
- Express.js for server layer

### Database
- PostgreSQL with Drizzle ORM
- Session storage support

## Contributing

1. The main development workflow runs on port 5000
2. Frontend changes auto-reload via Vite HMR
3. Backend changes require manual restart
4. CV content can be updated in `backend/data/cv.md`

## Deployment

The application is designed to run on Replit with automatic dependency management and port configuration. The production build serves static files through Express and proxies API requests to the Flask backend.
