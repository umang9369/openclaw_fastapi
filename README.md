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
