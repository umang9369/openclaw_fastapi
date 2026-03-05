@echo off
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Run: python -m venv venv
    exit /b 1
)

call venv\Scripts\activate.bat

echo [INFO] Removing deprecated google-generativeai SDK (if present)...
venv\Scripts\pip.exe uninstall google-generativeai -y -q 2>nul

echo [INFO] Installing / updating dependencies...
venv\Scripts\pip.exe install -r requirements.txt -q

echo [INFO] Starting OpenClaw FastAPI server on http://127.0.0.1:8000
echo [INFO] Docs available at: http://127.0.0.1:8000/docs
venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
