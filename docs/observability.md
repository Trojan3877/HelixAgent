# 📊 Observability in HelixAgent

HelixAgent implements the **3 pillars of observability**:

1. **Logging** → Structured logs via `loguru`
2. **Metrics** → Prometheus counters & histograms at `/metrics`
3. **Tracing** → OpenTelemetry spans for FastAPI routes

---

## Grafana Dashboard

A sample Grafana dashboard JSON is provided under `monitoring/grafana-dashboard.json`.

### Example Panels:
- Request Rate (Prometheus `helixagent_request_count`)
- Request Latency (95th percentile)
- Total Requests Counter

---

## Setup

1. Run Prometheus scraping FastAPI `/metrics`
2. Import the `grafana-dashboard.json` into Grafana
3. Visualize live metrics
