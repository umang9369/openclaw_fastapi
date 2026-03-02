

Project: Build an OpenClaw-Style Agent using FastAPI + OpenRouter You are a senior AI systems engineer. Your task is to generate a complete production-ready project. 🎯 OBJECTIVE Build an autonomous OpenClaw-style AI agent using: Python FastAPI OpenRouter API for LLM access ReAct (Reason → Ac

pasted

this is my project assist me devloping this step by step in easy way to make it

1:48 AM

Check available skills
Check available skills
Great! Let me build this project step by step for you. I'll create all the files now.


Created 14 files, ran a command
Created 14 files, ran a command

Create project folder structure

Script

Create .env.example
.env.example

Create config.py
config.py

Create openrouter_client.py
openrouter_client.py

Create memory.py
memory.py

Create prompts.py with tool definitions and system prompt
prompts.py

Create python_tool.py
python_tool.py

Create file_tool.py
file_tool.py

Create agent controller - the core ReAct loop
controller.py

Create main.py FastAPI server
main.py

Create requirements.txt
requirements.txt

Create __init__.py files for packages

Create services __init__.py

Create tools __init__.py

Create README.md
README.md
Done
Now let me copy everything to outputs:


Ran 2 commands, read a file
Ran 2 commands, read a file

Copy project to outputs

Script

Verify all files
bash

find /mnt/user-data/outputs/openclaw_fastapi -type f | sort
Output

/mnt/user-data/outputs/openclaw_fastapi/.env.example
/mnt/user-data/outputs/openclaw_fastapi/README.md
/mnt/user-data/outputs/openclaw_fastapi/agent/__init__.py
/mnt/user-data/outputs/openclaw_fastapi/agent/controller.py
/mnt/user-data/outputs/openclaw_fastapi/agent/memory.py
/mnt/user-data/outputs/openclaw_fastapi/agent/prompts.py
/mnt/user-data/outputs/openclaw_fastapi/config.py
/mnt/user-data/outputs/openclaw_fastapi/main.py
/mnt/user-data/outputs/openclaw_fastapi/requirements.txt
/mnt/user-data/outputs/openclaw_fastapi/services/__init__.py
/mnt/user-data/outputs/openclaw_fastapi/services/openrouter_client.py
/mnt/user-data/outputs/openclaw_fastapi/tools/__init__.py
/mnt/user-data/outputs/openclaw_fastapi/tools/file_tool.py
/mnt/user-data/outputs/openclaw_fastapi/tools/python_tool.py

Presented 11 files
Done
Your complete OpenClaw Agent project is ready! Here's a simple guide to get it running:

🚀 Quick Start (3 steps)
Step 1 — Set up Python environment

bash
cd openclaw_fastapi
python -m venv venv
source venv/bin/activate      # Mac/Linux
# OR: venv\Scripts\activate   # Windows
pip install -r requirements.txt
Step 2 — Add your API key

bash
cp .env.example .env
# Open .env and paste your OpenRouter API key
Get a free key at: openrouter.ai/keys

Step 3 — Start the server

bash
uvicorn main:app --reload --port 8000
🧪 Test It
Open http://localhost:8000/docs in your browser for interactive API docs, or use curl:

bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"goal": "Write python code to print fibonacci series up to 10 numbers and execute it"}'
📦 What Each File Does
File	Purpose
main.py	FastAPI server, /run-agent endpoint
config.py	Loads API key from .env
agent/controller.py	Core ReAct loop — reason → act → observe
agent/memory.py	Stores conversation history per session
agent/prompts.py	System prompt + tool definitions (JSON schema)
services/openrouter_client.py	Calls the LLM API async
tools/python_tool.py	Runs Python code safely via subprocess
tools/file_tool.py	Writes files to ./output/ directory
Want me to add any upgrade next — like web search, Docker support, or a streaming response feature?

Readme
Document · MD 
Main
PY 
Controller
PY 
Prompts
PY 
Memory
PY 
Openrouter client
PY 
Python tool
PY 
File tool
PY 
Config
PY 
Requirements
TXT 
.env
EXAMPLE 


safet#tool

Claude is AI and can make mistakes. Please double-check responses.
Readme · MD
Copy

# 🦾 OpenClaw — Autonomous ReAct AI Agent

An autonomous AI agent built with **FastAPI**, **OpenRouter**, and the **ReAct** (Reason → Act → Observe) loop. It can run Python code, write files, and solve complex goals step by step.

---

## 🏗 Architecture

```
User Request (HTTP POST)
        │
        ▼
  ┌─────────────┐
  │  FastAPI     │  main.py — REST API entry point
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Agent      │  controller.py — ReAct loop logic
  │  Controller  │
  └──────┬──────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 Memory     LLM Call
 (memory.py) (openrouter_client.py)
              │
              ▼
         Tool Calls?
         /         \
   run_python    write_file
  (python_tool) (file_tool)
         \         /
          ▼       ▼
        Result → Memory → Loop
                  │
                  ▼
           Final Answer
```

---

## 📁 Folder Structure

```
openclaw_fastapi/
├── main.py                    # FastAPI app + /run-agent endpoint
├── config.py                  # Loads .env variables
├── .env.example               # Template for API keys
├── requirements.txt           # Python dependencies
│
├── agent/
│   ├── controller.py          # Core ReAct agent loop
│   ├── memory.py              # Conversation memory store
│   └── prompts.py             # System prompt + tool definitions
│
├── services/
│   └── openrouter_client.py   # Async OpenRouter API client
│
└── tools/
    ├── python_tool.py         # Executes Python via subprocess
    └── file_tool.py           # Writes files safely
```

---

## ⚙️ Setup Instructions

### 1. Clone or create the project folder

```bash
cd openclaw_fastapi
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### 5. Run the server

```bash
uvicorn main:app --reload --port 8000
```

---

## 🧪 Test the API

### Health check
```bash
curl http://localhost:8000/health
```

### Run the agent
```bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"goal": "Write python code to print fibonacci series up to 10 numbers and execute it"}'
```

### Interactive API Docs
Open in browser: http://localhost:8000/docs

---

## 🔄 How It Works

1. You send a `POST /run-agent` request with a `goal`
2. The agent adds the system prompt + your goal to memory
3. It calls the LLM (via OpenRouter)
4. If the LLM wants to use a tool (e.g. `run_python`), the agent executes it
5. The result is stored in memory
6. The loop repeats until the LLM gives a final answer
7. The final answer is returned as JSON

---

## 📈 Future Roadmap

| Feature | Description |
|---|---|
| 🔍 Web Search Tool | Add DuckDuckGo or Brave Search API tool |
| 🧠 Vector DB Memory | Use ChromaDB or Pinecone for long-term memory |
| 🤖 Multi-Agent | Add planner + executor agents working together |
| 🌊 Streaming | Stream agent thoughts in real time via SSE |
| 🐳 Docker | Containerize with Dockerfile + docker-compose |
| 💰 Cost Tracking | Log token usage and estimated costs per run |
| 🔁 Self-Debugging | Auto-retry on code errors with reflection |
| 🖥 Dashboard | React/Next.js frontend to chat with agent |

---

## 🔒 Security Notes

- Python code runs via subprocess with a 10s timeout
- File writes are restricted to `./output/` directory
- Never expose this API publicly without authentication in production

