# api/main.py

"""
HelixAgent FastAPI Application
-------------------------------
Main API entrypoint. Mounts monitoring (Prometheus + OpenTelemetry) and
exposes core routes for agent inference.
"""

import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.monitoring import setup_monitoring

app = FastAPI(
    title="HelixAgent API",
    description="Modular AI agent framework for automation, reasoning, and decision-making.",
    version="1.0.0",
)

# Attach Prometheus metrics + OpenTelemetry tracing
setup_monitoring(app)


class PredictRequest(BaseModel):
    prompt: str


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to health check."""
    return JSONResponse({"status": "ok", "service": "HelixAgent"})


@app.get("/health", tags=["Operations"])
async def health():
    """Liveness / readiness probe for container orchestration."""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/predict", tags=["Agent"])
async def predict(payload: PredictRequest):
    """
    Run the agent on a user prompt.

    Body (JSON):
        { "prompt": "<your query>" }

    Returns:
        { "result": "<agent response>" }

    Note: Full agent integration (LangGraph + Java planner) is wired in
    agent/agent_core.py.  This endpoint serves as the HTTP interface; swap
    in AgenticAssistant().run(prompt) once the Java JAR and C++ .so are built.
    """
    # Placeholder response – replace with agent invocation once built:
    # from agent.agent_core import AgenticAssistant
    # result = AgenticAssistant().run(payload.prompt)
    result = f"[HelixAgent] received: {payload.prompt}"
    return {"result": result}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run("api.main:app", host=host, port=port, reload=False)
