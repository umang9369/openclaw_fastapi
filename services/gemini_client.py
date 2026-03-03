"""
services/gemini_client.py — Async client for the Google Gemini API.
Converts OpenAI-style messages/tools to Gemini format and returns
an OpenAI-compatible response dict so the agent controller needs no changes.
"""

import asyncio
import json
from typing import List, Dict, Optional

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-1.5-flash"


def _build_gemini_tools(tools: List[Dict]) -> List[Tool]:
    """Convert OpenAI function-calling format tools to Gemini Tool objects."""
    declarations = []
    for t in tools:
        fn = t["function"]
        declarations.append(
            FunctionDeclaration(
                name=fn["name"],
                description=fn.get("description", ""),
                parameters=fn.get("parameters", {}),
            )
        )
    return [Tool(function_declarations=declarations)]


def _convert_messages(messages: List[Dict]):
    """
    Convert OpenAI-style messages to Gemini history + system instruction.
    Returns (system_instruction: str | None, history: list, last_user_text: str)
    """
    system_instruction = None
    history = []
    last_user_text = ""

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")

        if role == "system":
            system_instruction = content
        elif role == "user":
            last_user_text = content
            history.append({"role": "user", "parts": [content]})
        elif role == "assistant":
            # May contain tool_calls — convert to model message
            text = content or ""
            tool_calls = msg.get("tool_calls", [])
            parts = []
            if text:
                parts.append(text)
            for tc in tool_calls:
                args = tc["function"].get("arguments", "{}")
                if isinstance(args, str):
                    args = json.loads(args)
                parts.append({"function_call": {"name": tc["function"]["name"], "args": args}})
            history.append({"role": "model", "parts": parts})
        elif role == "tool":
            # Tool result message
            tool_result = {
                "function_response": {
                    "name": msg.get("name", "tool"),
                    "response": {"output": content},
                }
            }
            history.append({"role": "user", "parts": [tool_result]})

    return system_instruction, history


def _to_openai_response(response) -> Dict:
    """
    Convert Gemini GenerateContentResponse to an OpenAI-compatible dict
    so the agent controller keeps working without changes.
    """
    candidate = response.candidates[0]
    parts = candidate.content.parts

    text_parts = []
    tool_calls = []

    for i, part in enumerate(parts):
        if hasattr(part, "function_call") and part.function_call.name:
            fc = part.function_call
            tool_calls.append({
                "id": f"call_{i}",
                "type": "function",
                "function": {
                    "name": fc.name,
                    "arguments": json.dumps(dict(fc.args)),
                },
            })
        elif hasattr(part, "text") and part.text:
            text_parts.append(part.text)

    finish_reason = "stop" if not tool_calls else "tool_calls"
    message = {
        "role": "assistant",
        "content": "\n".join(text_parts) if text_parts else None,
    }
    if tool_calls:
        message["tool_calls"] = tool_calls

    return {
        "choices": [
            {
                "message": message,
                "finish_reason": finish_reason,
            }
        ]
    }


async def call_llm(messages: List[Dict], tools: Optional[List[Dict]] = None) -> Dict:
    """
    Send messages to Gemini and return an OpenAI-compatible response dict.

    Args:
        messages: OpenAI-style message list (system/user/assistant/tool roles).
        tools: Optional OpenAI function-calling format tool definitions.

    Returns:
        OpenAI-compatible response dict with 'choices[0].message'.
    """
    system_instruction, history = _convert_messages(messages)

    model_kwargs = {
        "model_name": GEMINI_MODEL,
    }
    if system_instruction:
        model_kwargs["system_instruction"] = system_instruction
    if tools:
        model_kwargs["tools"] = _build_gemini_tools(tools)

    model = genai.GenerativeModel(**model_kwargs)

    # The last user message drives the current turn
    last_user_msg = history[-1]["parts"][0] if history else ""
    chat_history = history[:-1]  # everything before the last user message

    chat = model.start_chat(history=chat_history)

    def _send():
        return chat.send_message(last_user_msg)

    response = await asyncio.to_thread(_send)
    return _to_openai_response(response)
