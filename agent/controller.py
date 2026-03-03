import json
from agent.memory import Memory
from agent.prompts import SYSTEM_PROMPT, TOOLS
from services.gemini_client import call_llm
from tools.python_tool import run_python
from tools.file_tool import write_file

MAX_ITERATIONS = 10

class Agent:
    def __init__(self):
        self.memory = Memory()

    async def run(self, user_goal: str) -> str:
        self.memory.clear()
        self.memory.add("system", SYSTEM_PROMPT)
        self.memory.add("user", user_goal)

        for iteration in range(1, MAX_ITERATIONS + 1):
            print(f"\n[Agent] Iteration {iteration}/{MAX_ITERATIONS}")

            response = await call_llm(
                messages=self.memory.get(),
                tools=TOOLS,
            )

            choice = response.get("choices", [{}])[0]
            message = choice.get("message", {})
            finish_reason = choice.get("finish_reason", "")

            if finish_reason == "stop" or not message.get("tool_calls"):
                final_text = message.get("content") or "Task completed."
                print(f"[Agent] Final answer reached.")
                return final_text

            tool_calls = message.get("tool_calls", [])
            self.memory.add_raw(message)

            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_call_id = tool_call["id"]

                try:
                    args = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    args = {}

                print(f"[Agent] Calling tool: {tool_name} | args: {args}")

                try:
                    tool_result = self._execute_tool(tool_name, args)
                except Exception as e:
                    tool_result = f"Tool error: {str(e)}"

                print(f"[Agent] Tool result: {tool_result[:200]}")

                self.memory.add_raw({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_result,
                })

            self.memory.add(
                "user",
                "Reflect on the tool result. Is the task complete? If yes, give your final answer."
            )

        return "Max iterations reached without a final answer."

    def _execute_tool(self, tool_name: str, args: dict) -> str:
        if tool_name == "run_python":
            return run_python(args.get("code", ""))
        elif tool_name == "write_file":
            return write_file(
                filename=args.get("filename", "output.txt"),
                content=args.get("content", ""),
            )
        else:
            return f"ERROR: Unknown tool '{tool_name}'."