# Contributing to Agentic-AI-Assistant

First off, thank you for taking the time to contribute!  
This project is intended as a **capstone-level, production-grade reference** for autonomous-agent architectures.  
The guidelines below ensure consistent code quality, security, and documentation across Python, Java, and C++.

---

## 📋 Table of Contents
1. Getting Started
2. Development Workflow
3. Branching & Commit Style
4. Running Tests & Coverage
5. Building the Docker Image
6. Helm / Terraform / Ansible
7. Updating Documentation
8. Code of Conduct

---

## 1 – Getting Started

```bash
# Clone & create virtualenv
git clone https://github.com/Trojan3877/Agentic-AI-Assistant.git
cd Agentic-AI-Assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Build Java planner
cd agent/java && mvn -B package && cd ../../
# Compile C++ vector library (Linux/macOS)
g++ -O3 -shared -std=c++17 -fPIC agent/cpp/vector.cpp -o agent/cpp/libvector.so
