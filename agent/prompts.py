"""
agent/prompts.py — Defines the agent's system prompt and all available tools
in OpenAI function-calling format compatible with OpenRouter.
"""

SYSTEM_PROMPT ="""You are OpenClaw, an autonomous AI agent.

You think step by step and use tools to accomplish goals.

Your reasoning loop:
1. REASON — Think about what needs to be done.
2. ACT — Call the appropriate tool.
3. OBSERVE — Read the tool result carefully.
4. REFLECT — Decide if you're done or if you need another step.
5. ANSWER — When the task is complete, give a clear final answer.

Rules:
- Always use tools when you need to run code or save files.
- Never pretend to execute code — always use the run_python tool.
- After running a tool, reflect on the output before responding.
- If a tool fails, debug and retry with fixed code.
- Be concise but thorough in your final answer.
"""
# the above system prompt shows me the loop of the agent and the rules it should follow 
#also it helps me to show about the tools and how to use them, by using the RE-ACT process.


#tools definitions are below


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": (
                "Executes a Python code snippet in a sandboxed subprocess. "
                "Use this to run calculations, algorithms, data processing, or any Python logic. "
                "Returns stdout and stderr output."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Valid Python code to execute. Use print() to display results.",
                    }
                },
                "required": ["code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Writes text content to a file on disk. "
                "Use this to save code, results, reports, or any text output."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to create or overwrite (e.g. 'result.py').",
                    },
                    "content": {
                        "type": "string",
                        "description": "The full text content to write into the file.",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
]

