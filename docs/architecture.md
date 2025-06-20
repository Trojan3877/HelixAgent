# 🏗️ Agentic AI Assistant — System Architecture

## 1 – High-Level Overview
The Agentic AI Assistant is an autonomous, multi-tool agent designed to plan, execute, and evaluate complex tasks while logging production-grade metrics. It merges **three languages** to showcase full-stack ML engineering:

| Layer | Language | Key Role |
|-------|----------|----------|
| Planner | **Java 17** | Deterministic or LLM-enhanced task decomposition (`planner.jar`) |
| Orchestration | **Python 3.10** | LangGraph agent (`agent_core.py`) routes steps, handles memory and LLM calls |
| High-Perf Tool | **C++17** | `libvector.so` delivers ultrafast cosine-similarity and vector math |

## 2 – Execution Flow
```mermaid
flowchart LR
    A[User Prompt] --> B(Java Planner)<br/>createPlan()
    B --> C[LangGraph Graph]<br/>state machine
    C -->|vector_similarity| D[libvector.so (C++)]
    C -->|web_search|  E[DuckDuckGo API]
    C -->|snowflake_query| F[Snowflake]
    C -->|sagemaker_batch| G[SageMaker]
    C --> H[LLM (OpenAI / Bedrock)]
    H --> C
    C --> Z[Final Answer]
