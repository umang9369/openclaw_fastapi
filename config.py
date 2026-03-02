import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY : str = os.getenv("OPENROUTER_API_KEY","") 
MODEL_NAME : str = os.getenv("MODEL_NAME","")

if not OPENROUTER_API_KEY:
    raise EnvironmentError("OPENROUTER_API_KEY is not set in you .env file")

if not MODEL_NAME:
    raise EnvironmentError("MODEL_NAME is not set in you .env file")
