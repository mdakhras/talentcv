import type { Express } from "express";
import { createServer, type Server } from "http";
import { spawn } from "child_process";
import path from "path";

let flaskProcess: any = null;

export async function registerRoutes(app: Express): Promise<Server> {
  // Start Flask backend
  const startFlaskBackend = () => {
    if (flaskProcess) {
      flaskProcess.kill();
    }

    const backendPath = path.resolve(process.cwd(), 'backend');
    console.log(`Starting Flask backend from: ${backendPath}`);
    
    flaskProcess = spawn('python', ['app.py'], {
      cwd: backendPath,
      stdio: 'inherit',
      env: { 
        ...process.env, 
        PYTHONPATH: backendPath,
        FLASK_ENV: 'development'
      }
    });

    flaskProcess.on('error', (error: Error) => {
      console.error('Failed to start Flask backend:', error);
    });

    flaskProcess.on('exit', (code: number) => {
      console.log(`Flask backend exited with code ${code}`);
    });
  };

  // Start Flask backend in development
  if (process.env.NODE_ENV === 'development') {
    startFlaskBackend();
  }

  // Proxy API requests to Flask backend
  app.use('/api/*', (req, res) => {
    const apiUrl = `http://localhost:8000${req.originalUrl}`;
    
    // Forward the request to Flask
    fetch(apiUrl, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        ...req.headers,
      },
      body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
    })
    .then(response => response.json())
    .then(data => res.json(data))
    .catch(error => {
      console.error('Flask API Error:', error);
      res.status(500).json({ 
        error: 'Backend service unavailable',
        message: 'The Flask backend is not responding. Please ensure it is running on port 8000.'
      });
    });
  });

  const httpServer = createServer(app);

  // Cleanup on exit
  process.on('exit', () => {
    if (flaskProcess) {
      flaskProcess.kill();
    }
  });

  process.on('SIGINT', () => {
    if (flaskProcess) {
      flaskProcess.kill();
    }
    process.exit();
  });

  return httpServer;
}
