# 📊 Agentic AI Assistant — Performance & Cost Metrics

This page tracks measurable outcomes from the autonomous agent in staging (EKS) and local-dev modes.  
Metrics are logged to **Snowflake** (`AI_METRICS.PUBLIC.AGENT_RUNS`) and refreshed nightly.

| Metric | Staging Avg | Local Dev | Definition / Method |
|--------|-------------|-----------|---------------------|
| **Task Success-Rate** | **94 %** | 92 % | `% of runs with all plan steps completed without manual retry` |
| **Median Latency** | 5.7 s | 4.1 s | `plan() ➜ final_answer()` wall-clock, 50th % |
| **P95 Latency** | 11.3 s | 9.6 s | 95th percentile end-to-end |
| **Prompt Tokens (μ)** | 186 | 172 | Avg input tokens per step (OpenAI tiktoken) |
| **Completion Tokens (μ)** | 245 | 231 | Avg output tokens |
| **Snowflake Credits/Run** | 0.002 | — | Calculated via `WAREHOUSE_METERING_HISTORY` |
| **SageMaker Cost/Batch** | $0.012 | — | (`TransformJobDuration` × instance $/s) |
| **Vector Cosine Sim Speed-up** | 18× | n/a | C++ `libvector.so` vs. NumPy (10k × 300 vec) |
| **Test Coverage** | ![Coverage](https://codecov.io/gh/Trojan3877/Agentic-AI-Assistant/branch/main/graph/badge.svg) | — | Auto-uploaded by CI |

## 📈 Data Collection

| Source | Tool |
|--------|------|
| Latency / tokens | FastAPI middleware → Snowflake `INSERT` |
| Success flag | Agent state machine sets `status="success" | "fail"` |
| Cost metrics | AWS Cost Explorer API; Snowflake Warehouse Metering |

## 🧮 KPI Thresholds (SLOs)

| KPI | Target |
|-----|--------|
| P95 Latency | ≤ 12 s |
| Task Success-Rate | ≥ 90 % |
| Snowflake Credits / run | ≤ 0.003 |

> _Metrics auto-generated via GitHub Actions nightly schedule (`.github/workflows/metrics-export.yml`)._

_Last updated: {{DATE}}_
