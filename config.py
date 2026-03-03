"""
config.py — Loads environment variables for the entire application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "meta-llama/llama-3.3-70b-instruct:free")

if not OPENROUTER_API_KEY and not GEMINI_API_KEY:
    raise EnvironmentError("Neither OPENROUTER_API_KEY nor GEMINI_API_KEY is set in your .env file.")
