# BashAI - AI-Powered Bash Script Generator ⚡

[![Docker](https://img.shields.io/badge/Docker-Containers-blue?logo=docker)](https://www.docker.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-black)](https://deepseek.com)

A web application that converts natural language prompts into executable bash scripts using AI magic ✨

## Features 🌟
- Single-page web interface with prompt input
- AI-generated bash code execution
- Real-time results logging
- Docker-compose deployment
- Secure container isolation
- Persistent output storage

## Tech Stack 🛠️
- **Frontend**: Nginx + Vanilla JS
- **Backend**: Python FastAPI
- **AI Integration**: DeepSeek API
- **Infrastructure**: Docker Compose
- **Logging**: Structured JSON logs

## Quick Start 🚀
```bash
# 1. Clone repo
git clone https://github.com/yourusername/bashai.git
cd bashai

# 2. Create environment file
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env

# 3. Start services
docker-compose up --build -d

# 4. Access at http://localhost:8080



.
├── backend
│   ├── app.py          # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend
│   ├── index.html      # Web interface
│   └── nginx.conf      # Reverse proxy config
├── docker-compose.yml  # Container orchestration
├── logs                # Generated logs
└── bash_output         # Scripts & execution results




Security Notes 🔒
🔑 Always keep .env file private
🛡️ Never expose port 8080 to public internet
⚠️ Executes arbitrary code - use in isolated environments
🔄 Rotate API keys regularly

Next Improvement Suggestions 🚧
 Essential Enhancements
 Security Hardening
 Add JWT authentication
 Implement rate limiting
 Create user whitelist for prompts
 Error Handling
 Better AI output validation
 Script execution timeout control
 Safe directory sandboxing
UI Improvements
 Loading progress indicators
 Result preview before execution
 History browser
Advanced Features
 Support multiple languages (Python/Perl)
 Add environment variables to scripts
 Integrate with GitHub/GitLab
 Create cron job scheduler
 Add SMTP notifications
