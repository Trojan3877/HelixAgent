<div align="center">

# 🌀 HelixAgent

An **AI-powered agent framework** designed for modular automation, reasoning, and decision-making.  
Capstone-ready • Production-aware • Built for extensibility.

### 📊 Project Health & Features

![CI/CD](https://github.com/Trojan3877/HelixAgent/actions/workflows/ci.yml/badge.svg)
![Lint](https://github.com/Trojan3877/HelixAgent/actions/workflows/ci-cd.yml/badge.svg?label=Lint)
![Docker](https://img.shields.io/badge/Docker-ready-brightgreen?logo=docker&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-Packaged-brightgreen?logo=helm&logoColor=white)
![Observability](https://img.shields.io/badge/Monitoring-Prometheus%20%26%20OpenTelemetry-brightgreen?logo=prometheus&logoColor=white)
![Last Commit](https://img.shields.io/github/last-commit/Trojan3877/HelixAgent?logo=git&label=Last%20Commit&color=brightgreen)
![Repo Size](https://img.shields.io/github/repo-size/Trojan3877/HelixAgent?logo=github&label=Repo%20Size&color=brightgreen)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen?logo=github)
![Style](https://img.shields.io/badge/Code%20Style-Black-brightgreen?logo=python&logoColor=white)
![Docs](https://img.shields.io/badge/Docs-MkDocs%20Live-brightgreen?logo=readthedocs&logoColor=white)

</div>

---

## 📖 Overview

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

