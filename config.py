"""
config.py — Loads environment variables for the entire application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct")

if not OPENROUTER_API_KEY:
    raise EnvironmentError("OPENROUTER_API_KEY is not set in your .env file.")