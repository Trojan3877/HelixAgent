<div align="center">

# 🌀 HelixAgent

An **AI-powered agent framework** designed for modular automation, reasoning, and decision-making.  
Capstone-ready • Production-aware • Built for extensibility.

 HelixAgent — Autonomous AI Agent System

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-Agent%20Layer-blue?logo=typescript)
![Go](https://img.shields.io/badge/Go-Backend-blue?logo=go)
![LLM](https://img.shields.io/badge/LLM-Integrated-purple)
![Agents](https://img.shields.io/badge/AI-Agents-orange)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green)
![RAG](https://img.shields.io/badge/RAG-Pipeline-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Inference-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-blue?logo=kubernetes)
![Helm](https://img.shields.io/badge/Helm-Charts-blue?logo=helm)
![CI/CD](https://img.shields.io/badge/CI/CD-GitHub%20Actions-black?logo=githubactions)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)
![Ansible](https://img.shields.io/badge/Ansible-Automation-red?logo=ansible)
![Observability](https://img.shields.io/badge/Observability-Enabled-orange)
![Grafana](https://img.shields.io/badge/Grafana-Monitoring-orange?logo=grafana)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-yellow?logo=prometheus)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)
![Stars](https://img.shields.io/github/stars/Trojan3877/HelixAgent?style=social)
![Forks](https://img.shields.io/github/forks/Trojan3877/HelixAgent?style=social)
![Autonomous](https://img.shields.io/badge/Autonomous-Agents-critical)
![Multi-Agent](https://img.shields.io/badge/Multi--Agent-System-blue)
![Real-Time](https://img.shields.io/badge/Real--Time-Decisioning-green)
![Scalable](https://img.shields.io/badge/Scale-Horizontal-blue)
![Microservices](https://img.shields.io/badge/Architecture-Microservices-black)
![Latency](https://img.shields.io/badge/Latency-Low-critical)


HelixAgent is a **modular AI agent framework** that enables automation of tasks, reasoning chains, and integration with external APIs. It is designed for:

- 🤖 Building autonomous assistants
- 🧩 Extending with custom plugins and tools
- ⚡ Running fast experiments with structured logging and tracking
- ☁️ Deployment via Docker, Helm, and AWS EKS

### Architecture

```
Clients / UI (Streamlit dashboard, CLI)
         │
         ▼
  FastAPI API  (/predict, /health, /metrics)
         │
   ┌─────┼──────────┐
   ▼     ▼          ▼
Data   Agent    Monitoring
Ingest  Core    (Prometheus +
(pandas) (LangGraph  OpenTelemetry)
         + Java
         + C++)
         │
         ▼
 MLflow Experiment Tracking
```

---

## 🛠️ Prerequisites

| Tool | Version |
|------|---------|
| Python | ≥ 3.10 |
| pip | ≥ 23 |
| Docker | ≥ 24 (optional, for containers) |
| Docker Compose | ≥ 2.20 (optional) |
| Helm | ≥ 3.12 (optional, for Kubernetes) |
| Terraform | ≥ 1.6 (optional, for AWS EKS) |

---

## ⚙️ Local Development

### 1. Clone the repository

```bash
git clone https://github.com/Trojan3877/HelixAgent.git
cd HelixAgent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in your real credentials (never commit .env)
```

### 5. Start the API server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
# or via Makefile:
make dev
```

API is now available at <http://localhost:8000>. Interactive docs at <http://localhost:8000/docs>.

### 6. Run the CLI agent

```bash
python src/main.py --prompt "Summarise the latest data trends"
```

### 7. Run tests

```bash
pytest tests/ -v
# or with coverage:
make test
```

---

## 🌍 Environment Variable Reference

All configuration is driven by environment variables. Copy `.env.example` to `.env` and fill in your values.

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | API bind address | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `LOG_LEVEL` | Logging level (`DEBUG`/`INFO`/`WARNING`/`ERROR`) | `INFO` |
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier | — |
| `SNOWFLAKE_USER` | Snowflake username | — |
| `SNOWFLAKE_PASSWORD` | Snowflake password | — |
| `SNOWFLAKE_DATABASE` | Snowflake database name | `AGENT_DB` |
| `SNOWFLAKE_SCHEMA` | Snowflake schema | `PUBLIC` |
| `SNOWFLAKE_WAREHOUSE` | Snowflake warehouse | `COMPUTE_WH` |
| `AWS_DEFAULT_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | — |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | — |
| `MLFLOW_TRACKING_URI` | MLflow tracking server URI | `http://127.0.0.1:5000` |
| `MLFLOW_EXPERIMENT_NAME` | MLflow experiment name | `HelixAgent-Experiments` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | — |

---

## 🐳 Docker

### Build and run with Docker

```bash
# Build
docker build -t helixagent:latest .
# or: make build

# Run
docker run -p 8000:8000 --env-file .env helixagent:latest
# or: make run
```

### Run with Docker Compose (includes PostgreSQL)

```bash
# Copy and edit env file
cp .env.example .env

# Start all services
docker compose up -d

# Stop
docker compose down
```

Services started:
- **agent** on <http://localhost:8000> (FastAPI)
- **db** on `localhost:5432` (PostgreSQL – local Snowflake stand-in)

---

## ☸️ Kubernetes (Helm)

### Deploy to an existing cluster

```bash
# Deploy / upgrade
make helm-up

# Uninstall
make helm-uninstall
```

The Helm chart is located in `infra/helm/agentic-ai-assistant/`. Review `values.yaml` to customise replicas, resources, image tag, and environment values.

### Provision AWS EKS + deploy via Terraform

```bash
# Initialise
make tf-init

# Review plan
make tf-plan

# Apply (creates EKS cluster + Helm release)
make tf-apply

# Destroy
make tf-destroy
```

> **Note**: Set `vpc_id` and `public_subnet_ids` in `infra/terraform/main.tf` or via `-var` flags before applying.

---

## 📊 Observability

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Liveness / readiness probe |
| `GET /metrics` | Prometheus metrics scrape endpoint |

A Grafana dashboard JSON is provided at `monitoring/grafana-dashboard.json` and can be imported into any Grafana instance.

---

## 📘 Examples

Ready-to-run Jupyter notebooks are in the [`examples/`](examples/) directory:

- **Quickstart** – logger, data pipeline, MLflow tracking
- **Training Demo** – simulated training loop with metrics
- **Inference Demo** – query FastAPI endpoints
- **Monitoring Demo** – scrape Prometheus metrics

---

## 🧹 Code Quality

```bash
# Format
black src/ api/ tests/
isort src/ api/ tests/

# Lint
flake8 src/ api/ tests/

# All (via pre-commit)
pre-commit run --all-files
```

Pre-commit hooks are configured in `.pre-commit-config.yaml` and enforce Black, isort, and Flake8 on every commit.

---

## 📑 Documentation

Full documentation is built with MkDocs:

```bash
mkdocs serve          # local preview at http://127.0.0.1:8000
mkdocs gh-deploy      # deploy to GitHub Pages
```

---

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

