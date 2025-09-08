# api/monitoring.py

"""
Monitoring for HelixAgent
-------------------------
Provides Prometheus metrics and OpenTelemetry tracing integration.
"""

from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# -----------------------------
# Prometheus Metrics
# -----------------------------
REQUEST_COUNT = Counter(
    "helixagent_request_count",
    "Total number of requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "helixagent_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
)


def setup_monitoring(app: FastAPI):
    """Attach monitoring endpoints and tracing to FastAPI"""

    # Prometheus /metrics endpoint
    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    # Middleware for metrics
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        import time
        start = time.time()

        response = await call_next(request)
        latency = time.time() - start

        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.url.path, status_code=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)

        return response

    # -----------------------------
    # OpenTelemetry Tracing
    # -----------------------------
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    span_processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Auto-instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    return app
