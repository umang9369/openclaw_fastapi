from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent.controller import Agent

app = FastAPI(
    title="OpenClaw FastAPI",
    description="An Autonomous Agent System for OpenRouter using Fastapi",
    version="1.0.0",
)

class AgentRequest(BaseModel):
    goal: str = Field(..., description="The goal of the agent")

class AgentResponse(BaseModel):
    response: str = Field(..., description="The response of the agent")

@app.post("/run-agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Run the OpenClaw agent with a user-defined goal.

    The agent will reason, call tools (run Python, write files), 
    observe results, and return a final answer.

    """

    if not request.goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty")

    agent = Agent(goal=request.goal)
    try:
        result = await agent.run(user_goal=request.goal)
        return AgentResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """
    Health check endpoint

    """
    return {"status": "ok", "agent": "OpenClaw v1.0"}
