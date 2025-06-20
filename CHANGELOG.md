# Changelog
All notable changes to **Agentic-AI-Assistant** will be documented in this file.

The project adheres to **Semantic Versioning 2.0.0**  
and the **Keep a Changelog** format.

---

## [Unreleased]
### Added
- Issue & PR GitHub templates
- Contributor guide (`CONTRIBUTING.md`)
- Code of Conduct (Contributor Covenant v2.1)
- Helm chart (`infra/helm/agentic-ai-assistant`)
- Terraform module for EKS + Helm deploy
- Ansible playbook for Helm upgrade
- CI pipeline: Java + C++ build, pytest coverage → Codecov
- Docs: `architecture.md`, `metrics.md`, flow-chart image
- Multilanguage agent core (Python + Java + C++)
- Snowflake, SageMaker, and Web-Search tool modules
- FastAPI wrapper (`app/api.py`)

---

## [1.0.0] – 2025-06-20
### Added
- Initial public release:
  - Java task planner (`planner.jar`)
  - C++ cosine-similarity library (`libvector.so`)
  - Python LangGraph orchestrator (`agent_core.py`)
  - Dockerfile (multi-language runtime)
  - Unit tests and coverage badge
  - README with badges, quick-start, and architecture flow-chart

[Unreleased]: https://github.com/Trojan3877/Agentic-AI-Assistant/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Trojan3877/Agentic-AI-Assistant/releases/tag/v1.0.0
