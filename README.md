# 🦾 OpenClaw — Autonomous ReAct AI Agent

An autonomous AI agent built with **FastAPI**, **Google Gemini**, and the **ReAct** (Reason → Act → Observe) loop. It can run Python code, write files, and solve complex goals step by step.

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
 (memory.py) (gemini_client.py)
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
│   └── gemini_client.py       # Async Google Gemini API client
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
# Edit .env and add your Google Gemini API key
```

Your `.env` should look like:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You can get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Run the server

```bash
uvicorn main:app --reload --port 8000
```

---

## 🔄 How It Works

1. You send a `POST /run-agent` request with a `goal`
2. The agent adds the system prompt + your goal to memory
3. It calls the LLM (via Google Gemini)
4. If the LLM wants to use a tool (e.g. `run_python`), the agent executes it
5. The result is stored in memory
6. The loop repeats until the LLM gives a final answer
7. The final answer is returned as JSON

---

## 🔒 Security Notes

- Python code runs via subprocess with a 10s timeout
- File writes are restricted to `./output/` directory
- Never expose this API publicly without authentication in production
