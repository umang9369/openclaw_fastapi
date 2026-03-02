"""
services/openrouter_client.py — Async HTTP client for the OpenRouter LLM API.
"""
#this basically makes a call to the api of openrouter and gets the response from the model

import httpx
from typing import List, Dict, Optional
from config import OPENROUTER_API_KEY, MODEL_NAME

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openclaw-agent.local",
    "X-Title": "OpenClaw FastAPI Agent",
}

async def call_llm(messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
    """
    Send messages to the OpenRouter API and return the full JSON response.

    Args:
        messages: List of chat messages (role + content).
        tools: Optional list of tool definitions in OpenAI function-calling format.

    Returns:
        Parsed JSON response dict from the API.

    Raises:
        Exception: On HTTP errors or unexpected response structure.
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
    }

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(OPENROUTER_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenRouter API error {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Network error contacting OpenRouter: {str(e)}")
