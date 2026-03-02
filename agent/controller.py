"""
Controller for the OpenClaw Agent

This is the core ReAct agent loop.
matlab 1- call krega llm ko with prompt// 2- llm decide krega ki kis tool ko use krke kya krwana h
and then in last agent(tool execute hoga) final answer llm ko return krega

"""
import json
from typing import Optional

from agent.memory import Memory
from agent.prompts import SYSTEM_PROMPT,TOOLS
from services.openrouter_client import call_llm
from tools.python_tool import run_python
from tools.file_tool import write_file

MAX_ITERATIONS = 10 
#just to prevent it from going into infinite loop

class Agent:
    """
    OpenClaw ReAct Agent.
    Reasons, acts with tools, observes results, and loops until done.
    """
    def __init__(self):
        self.memory=Memory()
        
    async def run (self , user_goal : str) -> str:
        """
        Run the agent loop for a given user goal.

        Args:
            user_goal: Natural language task description from the user.

        Returns:
            The agent's final answer as a string.
        """
        self.memory.clear()

        self.memory.add("system",SYSTEM_PROMPT)
        self.memory.add("user",user_goal)

        for iteration in range(1,MAX_ITERATIONS+1):
            printf(f"\n[agent] iteration {iteration}/{MAX_ITERATIONS}")
            
            response=await call_llm(
                messages=self.memory.get_messages(),
                tools=TOOLS,
                tool_choice="auto"
            )
            #memory call hoga by llm
            if finish_reason == "stop" or not message.get("tool_calls"):
                final_text = message.get("content") or "Task completed."
                print(f"[Agent] Final answer reached.")
                return final_text
            #final answer comes here

            tool_calls = message.get("tool_calls", [])

            self.memory.add_raw(message)  #this add everything into memory.

            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_call_id = tool_call["id"]

                # Safely parse arguments
                try:
                    args = json.loads(tool_call["function"]["arguments"])
                except json.JSONDecodeError:
                    args = {}

                print(f"[Agent] Calling tool: {tool_name} | args: {args}")

                #Execute Tool 
                tool_result = self._execute_tool(tool_name, args)
                print(f"[Agent] Tool result: {tool_result[:200]}...")
in
                # Store tool result by making it in OpenAI tool format
                self.memory.add_raw({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_result,
                })