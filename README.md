![Capstone](https://img.shields.io/badge/Project-Capstone-blueviolet)
![Build](https://github.com/Trojan3877/Agentic-AI-Assistant/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/Trojan3877/Agentic-AI-Assistant/branch/main/graph/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Java](https://img.shields.io/badge/Java-17-red?logo=openjdk)
![C++](https://img.shields.io/badge/C%2B%2B-17-lightgrey?logo=c%2B%2B)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Helm](https://img.shields.io/badge/Helm-Chart-informational)
![Terraform](https://img.shields.io/badge/Terraform-EKS-critical)
![Ansible](https://img.shields.io/badge/Ansible-Automation-red)










# -Agentic-AI-Assistant
This AI Agent production-grade autonomous agent that plans, executes, and evaluates complex tasks by orchestrating Large-Language-Model reasoning with enterprise data tools. Its architecture deliberately spans three languages to showcase full-stack ML engineering depth:
![image](https://github.com/user-attachments/assets/baa6a592-895f-4407-8104-9c00fbe76a1a)

# 🤖 Agentic-AI-Assistant


### 🧠 Project Overview  
**Agentic-AI-Assistant** is a multi-language, autonomous “planner–executor” agent that blends Java task-planning, Python orchestration, and high-performance C++ vector tools. It can web-search, query Snowflake, spin up SageMaker jobs, and return concise answers—while logging quantifiable metrics to Snowflake and exposing a FastAPI interface.

## 🔍 Core AI / ML Algorithms Used

| Badge | Algorithm / Component | Where It’s Used | Purpose |
|-------|-----------------------|-----------------|---------|
| ![LLM](https://img.shields.io/badge/Model-LLM-orange) | **Large Language Model (GPT-3.5 / GPT-4 / Bedrock)** | `agent_core.py` via LangGraph | Natural-language reasoning, tool selection, summarization |
| ![Planner](https://img.shields.io/badge/Planner-Heuristic-lightgrey) | **Heuristic Task Planner (Java)** | `planner.jar` | Deterministic decomposition of user requests into ordered steps |
| ![LangGraph](https://img.shields.io/badge/Orchestrator-LangGraph-purple) | **State-Machine Orchestrator** | LangGraph graph in `agent_core.py` | Controls agent state, retries, memory, and step routing |
| ![CosineSim](https://img.shields.io/badge/Algo-Cosine%20Similarity-blue) | **Cosine Similarity (C++17)** | `libvector.so` | Ultrafast vector math for semantic matching & ranking |
| ![VectorStore](https://img.shields.io/badge/VectorStore-FAISS-green) | **FAISS Embedding Retrieval** | `memory.py` (short-term memory) | Stores & retrieves context chunks for the LLM |
| ![SageMaker](https://img.shields.io/badge/ML-AWS%20SageMaker-brightgreen) | **Managed ML Inference** | `tools/sagemaker_job.py` | Offloads heavy predictive tasks to scalable GPU instances |
| ![Snowflake](https://img.shields.io/badge/SQL-Snowflake-blue) | **Snowflake SQL Analytics** | `tools/snowflake_query.py` | Feature aggregation, cost & KPI logging |


---

## 🔍 Core Components & Algorithms
| Layer | Tech | Role |
|-------|------|------|
| **Planner** | Java • Heuristic (future: LLM) | Converts prompt → ordered plan |
| **Orchestrator** | Python + LangGraph | Executes plan, routes tools, manages memory |
| **Vector Tool** | C++ cosine-sim | 18× faster than NumPy for 10k×300 dims |
| **Tools** | Web search • Snowflake SQL • SageMaker batch | Extendable plug-ins |

---

## 🏗 Architecture Diagram  
![Flow-chart](docs/flowchart.png)

Detailed explanation in **[`docs/architecture.md`](docs/architecture.md)**.

---

## 📈 Metrics Snapshot  
See **[`docs/metrics.md`](docs/metrics.md)** for live Snowflake-logged KPIs.

| KPI | Current | SLO |
|-----|---------|-----|
| Task Success | **94 %** | ≥ 90 % |
| P95 Latency  | 11.3 s  | ≤ 12 s |
| Coverage     | ![Coverage](https://codecov.io/gh/Trojan3877/Agentic-AI-Assistant/branch/main/graph/badge.svg) | ≥ 80 % |

---

## 🚀 Quick Start

### Local Dev
```bash
git clone https://github.com/Trojan3877/Agentic-AI-Assistant.git
cd Agentic-AI-Assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# compile C++ lib / build planner.jar if needed
uvicorn app.api:app --reload

## 📂 File Structure


---

## 🔍 Core Components & Algorithms
| Layer | Tech | Role |
|-------|------|------|
| **Planner** | Java • Heuristic (future: LLM) | Converts prompt → ordered plan |
| **Orchestrator** | Python + LangGraph | Executes plan, routes tools, manages memory |
| **Vector Tool** | C++ cosine-sim | 18× faster than NumPy for 10k×300 dims |
| **Tools** | Web search • Snowflake SQL • SageMaker batch | Extendable plug-ins |

---

## 🏗 Architecture Diagram  
![Flow-chart](docs/flowchart.png)

Detailed explanation in **[`docs/architecture.md`](docs/architecture.md)**.

---

## 📈 Metrics Snapshot  
See **[`docs/metrics.md`](docs/metrics.md)** for live Snowflake-logged KPIs.

| KPI | Current | SLO |
|-----|---------|-----|
| Task Success | **94 %** | ≥ 90 % |
| P95 Latency  | 11.3 s  | ≤ 12 s |
| Coverage     | ![Coverage](https://codecov.io/gh/Trojan3877/Agentic-AI-Assistant/branch/main/graph/badge.svg) | ≥ 80 % |

---

## 🚀 Quick Start

### Local Dev
```bash
git clone https://github.com/Trojan3877/Agentic-AI-Assistant.git
cd Agentic-AI-Assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# compile C++ lib / build planner.jar if needed
uvicorn app.api:app --reload


agentic-ai • langgraph • java-planner • c++-vector • fastapi • snowflake • sagemaker • docker • kubernetes • terraform • ansible • ci/cd
