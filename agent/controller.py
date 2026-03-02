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

            

            self.memory.add("assistant",)
