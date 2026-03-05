"""
services/gemini_client.py

Uses the new google-genai SDK (pip install google-genai).
Docs: https://googleapis.github.io/python-genai/
"""
import json
import uuid
import logging
from typing import List, Dict, Optional

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, MODEL_NAME

logger = logging.getLogger(__name__)

# One global async-capable client
_client = genai.Client(api_key=GEMINI_API_KEY)


def _build_genai_tool(tools: Optional[List[Dict]]) -> Optional[types.Tool]:
    """Convert OpenAI-style tool list into a google.genai types.Tool."""
    if not tools:
        return None

    type_map = {
        "string":  types.Type.STRING,
        "integer": types.Type.INTEGER,
        "number":  types.Type.NUMBER,
        "boolean": types.Type.BOOLEAN,
        "array":   types.Type.ARRAY,
        "object":  types.Type.OBJECT,
    }

    fn_decls = []
    for tool in tools:
        fn = tool.get("function", {})
        params = fn.get("parameters", {})

        properties = {
            name: types.Schema(
                type=type_map.get(schema.get("type", "string").lower(), types.Type.STRING),
                description=schema.get("description", ""),
            )
            for name, schema in params.get("properties", {}).items()
        }

        fn_decls.append(
            types.FunctionDeclaration(
                name=fn.get("name", ""),
                description=fn.get("description", ""),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties=properties,
                    required=params.get("required", []),
                ),
            )
        )

    return types.Tool(function_declarations=fn_decls)


async def call_llm(
    messages: List[Dict],
    tools: Optional[List[Dict]] = None,
) -> Dict:
    """
    Call Gemini using the new google-genai async API.

    Returns an OpenAI-compatible dict:
      choices[0].message.{role, content, tool_calls}
      choices[0].finish_reason  →  "stop" | "tool_calls"
    """
    # ── Separate system prompt from conversation turns ──────────────────────
    system_parts: List[str] = []
    contents: List[Dict] = []          # plain dicts — SDK accepts these fine

    for msg in messages:
        role = msg.get("role", "")
        text = msg.get("content") or ""

        if role == "system":
            system_parts.append(text)
        elif role == "user":
            contents.append({"role": "user", "parts": [{"text": text}]})
        elif role == "assistant":
            contents.append({"role": "model", "parts": [{"text": text}]})
        # role="tool" already converted to user turns by the controller

    if not contents:
        raise ValueError("No user messages found to send to the model.")

    system_instruction = "\n\n".join(system_parts) if system_parts else None

    # ── Build GenerateContentConfig ─────────────────────────────────────────
    genai_tool = _build_genai_tool(tools)

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[genai_tool] if genai_tool else None,
        # Disable automatic tool dispatch — we handle it ourselves
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ) if genai_tool else None,
    )

    # ── Call the API (natively async via client.aio) ────────────────────────
    try:
        response = await _client.aio.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )
    except Exception as e:
        logger.error("Gemini generate_content failed: %s", e, exc_info=True)
        raise Exception(f"Gemini API error: {e}")

    # ── Parse response parts ────────────────────────────────────────────────
    tool_calls: Optional[List[Dict]] = None
    text_content = ""

    try:
        candidate = response.candidates[0] if response.candidates else None
        if candidate and candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                fc = getattr(part, "function_call", None)
                if fc and getattr(fc, "name", None):
                    if tool_calls is None:
                        tool_calls = []
                    tool_calls.append({
                        "id": f"call_{uuid.uuid4().hex[:8]}",
                        "type": "function",
                        "function": {
                            "name": fc.name,
                            "arguments": json.dumps(dict(fc.args or {})),
                        },
                    })
                else:
                    text_content += getattr(part, "text", "") or ""
    except Exception as e:
        logger.warning("Error parsing Gemini response parts: %s", e)

    # Fallback: try response.text directly
    if not text_content and not tool_calls:
        try:
            text_content = response.text or ""
        except Exception:
            text_content = ""

    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": text_content,
                "tool_calls": tool_calls,
            },
            "finish_reason": "tool_calls" if tool_calls else "stop",
        }]
    }
