# ==============================
# HelixAgent Dockerfile
# ==============================

# ── Stage 1: Build Java planner JAR ─────────────────────────────────────────
FROM maven:3.9-eclipse-temurin-11-slim AS java-builder
WORKDIR /build
COPY java/ java/
RUN cd java && mvn package -q

# ── Stage 2: Runtime image ──────────────────────────────────────────────────
FROM python:3.10-slim

WORKDIR /app

# System dependencies (C++ compiler for libvector.so)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Compile C++ cosine-similarity library
RUN g++ -O3 -shared -std=c++17 -fPIC agent/cpp/vector.cpp -o agent/cpp/libvector.so

# Copy compiled Java planner JAR from build stage
COPY --from=java-builder /build/java/target/planner.jar agent/java/planner.jar

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Default command: start FastAPI app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
