
# CV Chatbot

## Overview

This is an AI-powered CV chatbot application that provides an interactive interface for users to learn about Mohammed Alakhras's professional background. The system consists of a React frontend with TypeScript, a Node.js/Express server layer, and a Flask backend that uses CrewAI agents and Azure OpenAI for intelligent question answering about CV content.

## Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                    (React + TypeScript)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/WS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Node.js/Express Server                         │
│                      (Port 5000)                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Vite Dev Server (HMR)                                 │  │
│  │  • Static File Serving                                   │  │
│  │  • API Proxy to Flask Backend                           │  │
│  │  • Session Management                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ Proxy /api/*
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Flask Backend (Python)                         │
│                      (Port 5001)                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  CV Processing Pipeline:                                 │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │  │
│  │  │ CV Loader   │→ │ CV Retriever │→ │ CrewAI Agents │  │  │
│  │  │ (Markdown)  │  │ (TF-IDF/     │  │ - Researcher  │  │  │
│  │  │             │  │  Embeddings) │  │ - Analyst     │  │  │
│  │  └─────────────┘  └──────────────┘  └───────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
│  ┌──────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │ Azure OpenAI     │  │ PostgreSQL      │  │ CV Data      │  │
│  │ (LLM & Embeddings│  │ (Optional DB)   │  │ (cv.md)      │  │
│  └──────────────────┘  └─────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Frontend Layer
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast HMR and optimized builds
- **UI Components**: Shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS with custom theme
- **State Management**: TanStack Query for server state
- **Routing**: Wouter for lightweight routing

#### Server Layer (Node.js)
- **Express.js**: HTTP server and API gateway
- **Port**: 5000 (production ready)
- **Responsibilities**:
  - Serve React frontend (static files in production)
  - Proxy API requests to Flask backend
  - Session management with PostgreSQL store
  - Development mode Vite integration

#### Backend Layer (Python/Flask)
- **Port**: 5001
- **Core Components**:
  - **CV Loader**: Parses markdown CV into structured sections
  - **CV Retriever**: TF-IDF search with optional Azure embeddings
  - **CrewAI Agents**: Multi-agent AI system for intelligent responses
    - Researcher: Retrieves relevant CV information
    - Analyst: Structures and refines responses
  
#### Data Flow
1. User asks question via React UI
2. Request sent to Node.js server (port 5000)
3. Node.js proxies to Flask backend (port 5001)
4. Flask processes query through CV Retriever
5. CrewAI agents orchestrate response generation
6. Azure OpenAI (optional) enhances responses
7. Response returned through proxy to frontend
8. UI displays answer with citations

## Features

- Interactive chat interface for CV questions
- Multi-agent AI system for intelligent responses
- Section-based CV content organization
- Suggested questions by CV section
- Citation support showing information sources
- Responsive design with dark/light themes
- Fallback to TF-IDF when Azure OpenAI unavailable

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- PostgreSQL database (optional, for user management)
- Azure OpenAI API access (optional, for enhanced AI responses)

## Environment Variables

Create a `.env` file in the root directory. See `.env.example` for all available options:

```bash
# Azure OpenAI Configuration (Optional)
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Flask Configuration
FLASK_PORT=5001
FLASK_ENV=development

# Database Configuration (Optional)
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Session Configuration
SESSION_SECRET=your_random_secret_key_here

# Application Settings
PORT=5000
NODE_ENV=development
LOG_LEVEL=INFO
```

## Running Locally

### Quick Start (Recommended)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd cv-chatbot
```

2. **Copy environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Install dependencies**:
```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd backend
pip install -r requirements.txt
cd ..
```

4. **Start the application**:
```bash
# Development mode (runs both frontend and backend)
npm run dev
```

This will start:
- Node.js server on `http://0.0.0.0:5000`
- Flask backend on `http://0.0.0.0:5001`
- Vite dev server with hot module replacement

5. **Access the application**:
Open your browser to `http://localhost:5000`

### Manual Setup (Alternative)

If you prefer to run frontend and backend separately:

**Terminal 1 - Backend**:
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend**:
```bash
npm run dev
```

### Production Build

```bash
# Build the frontend
npm run build

# Start production server
npm start
```

The production server serves optimized static files and proxies API requests to the Flask backend.

## Running with Docker

### Docker Setup

1. **Create Dockerfile** in the root directory:

```dockerfile
FROM node:18-alpine AS frontend-build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM python:3.11-slim

# Install Node.js for running the server
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements and install
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY --from=frontend-build /app/dist ./dist
COPY --from=frontend-build /app/server ./server
COPY --from=frontend-build /app/package*.json ./
COPY backend ./backend

# Install production Node.js dependencies
RUN npm ci --only=production

EXPOSE 5000
EXPOSE 5001

CMD ["sh", "-c", "python backend/app.py & npm start"]
```

2. **Create docker-compose.yml**:

```yaml
version: '3.8'

services:
  cv-chatbot:
    build: .
    ports:
      - "5000:5000"
      - "5001:5001"
    environment:
      - NODE_ENV=production
      - FLASK_ENV=production
      - PORT=5000
      - FLASK_PORT=5001
    env_file:
      - .env
    volumes:
      - ./backend/data:/app/backend/data
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: cvdb
      POSTGRES_USER: cvuser
      POSTGRES_PASSWORD: cvpassword
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

3. **Build and run**:

```bash
# Build the Docker image
docker-compose build

# Start the services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the services
docker-compose down
```

4. **Access the application**:
Visit `http://localhost:5000`

### Docker Commands Reference

```bash
# Rebuild after code changes
docker-compose up -d --build

# View running containers
docker-compose ps

# Execute commands in container
docker-compose exec cv-chatbot bash

# Remove all containers and volumes
docker-compose down -v
```

## Deploying to Replit Cloud

Replit provides seamless deployment with automatic dependency management and scaling.

### Quick Deploy

1. **Import to Replit**:
   - Go to [Replit](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Paste your repository URL

2. **Configure Environment Variables**:
   - Open the "Secrets" tool (🔒 icon in sidebar)
   - Add your environment variables:
     - `AZURE_OPENAI_API_KEY`
     - `AZURE_OPENAI_ENDPOINT`
     - `AZURE_OPENAI_DEPLOYMENT_NAME`
     - `SESSION_SECRET`

3. **Run the Application**:
   - Click the "Run" button
   - Replit will automatically:
     - Install Node.js dependencies
     - Install Python dependencies
     - Start both servers

4. **Deploy to Production**:
   - Click "Deploy" button in the top right
   - Choose "Autoscale Deployment" (recommended)
   - Configure deployment settings:
     - Build command: `npm run build`
     - Run command: `npm start`
   - Click "Deploy"

### Deployment Options on Replit

#### Autoscale Deployment (Recommended)
- **Best for**: Web applications with variable traffic
- **Features**: 
  - Scales down to save costs
  - Scales up automatically under load
  - 99.95% uptime SLA
- **Pricing**: Pay-per-use based on traffic

#### Reserved VM Deployment
- **Best for**: Applications requiring consistent resources
- **Features**:
  - Dedicated VM
  - Predictable costs
  - 99.9% uptime
- **Pricing**: Fixed monthly cost

#### Static Deployment
- **Best for**: Frontend-only deployments
- **Not suitable** for this full-stack application

### Post-Deployment Configuration

1. **Custom Domain** (optional):
   - Go to Deployments → Settings
   - Add your custom domain
   - Update DNS records as instructed

2. **Environment Variables**:
   - Use Replit Secrets for production
   - Never commit sensitive data to `.env`

3. **Database Setup** (if using PostgreSQL):
   - Enable PostgreSQL from the Replit database tab
   - Update `DATABASE_URL` in Secrets

4. **Monitor Deployment**:
   - View logs in Deployments tab
   - Check health at `/api/health`
   - Monitor metrics and costs

### Troubleshooting Deployment

**Port Issues**:
- Ensure backend runs on port 5001: `FLASK_PORT=5001`
- Node.js server must use port 5000: `PORT=5000`

**Backend Not Starting**:
- Check Python dependencies in console
- Verify CV file exists: `backend/data/cv.md`
- Review Flask logs for errors

**Azure OpenAI Errors**:
- Verify API key in Secrets
- Check endpoint URL format
- Ensure deployment name is correct
- Application will fallback to TF-IDF if unavailable

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
│   │   ├── agents.py      # Agent definitions
│   │   ├── tasks.py       # Task definitions
│   │   └── tools.py       # CV search tools
│   ├── data/              # CV data files
│   │   └── cv.md          # CV content
│   ├── app.py             # Flask application
│   ├── retriever.py       # CV search and retrieval
│   └── loader.py          # CV content processing
└── shared/                # Shared TypeScript schemas
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/sections` - Get available CV sections
- `GET /api/questions?section={section}` - Get suggested questions
- `POST /api/ask` - Ask a question about the CV
  ```json
  {
    "question": "What AI projects has Mohammed worked on?",
    "section": "Experience"  // optional
  }
  ```

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
- scikit-learn for TF-IDF text processing
- BeautifulSoup for HTML parsing
- Express.js for Node.js server layer

### Database
- PostgreSQL with Drizzle ORM (optional)
- Session storage support

## Development Workflow

1. **Development Mode**:
   - Frontend changes auto-reload via Vite HMR
   - Backend changes require manual restart
   - Both servers run in parallel

2. **Updating CV Content**:
   - Edit `backend/data/cv.md`
   - Restart Flask backend
   - Changes reflected immediately

3. **Adding Features**:
   - Frontend: Add components in `client/src/components/`
   - Backend: Extend agents in `backend/crew/`
   - API: Update `server/routes.ts` and `backend/app.py`

## Known Issues

1. **Port Conflicts**: If port 5000 or 5001 is in use, update environment variables
2. **Azure OpenAI Fallback**: System uses TF-IDF when Azure credentials are unavailable
3. **Session Storage**: PostgreSQL required for persistent sessions across restarts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `npm run dev`
5. Submit a pull request

## License

MIT

## Support

For issues and questions:
- Check existing GitHub issues
- Review Replit deployment logs
- Contact: md.alakhras@gmail.com
