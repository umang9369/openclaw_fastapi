import asyncio
import google.generativeai as genai
from typing import List, Dict, Optional
from config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

async def call_llm(messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
    model = genai.GenerativeModel(MODEL_NAME)

    # Convert messages to Gemini format
    history = []
    system_text = ""

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content") or ""

        if role == "system":
            system_text = content
        elif role == "user":
            history.append({"role": "user", "parts": [content]})
        elif role == "assistant":
            history.append({"role": "model", "parts": [content]})

    # Add system prompt to the first user message
    if system_text and history:
        history[0]["parts"][0] = system_text + "\n\n" + history[0]["parts"][0]

    if not history:
        raise ValueError("No user messages found to send to the model.")

    try:
        chat_history = history[:-1] if len(history) > 1 else []
        last_message = history[-1]["parts"][0]

        # Run synchronous Gemini SDK call in a thread pool to avoid blocking the event loop
        def _send():
            chat = model.start_chat(history=chat_history)
            return chat.send_message(last_message)

        response = await asyncio.to_thread(_send)

        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response.text,
                    "tool_calls": None,
                },
                "finish_reason": "stop",
            }]
        }
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")
