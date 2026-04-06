# --------------------------------------------------------------------
# Agentic AI Assistant – Makefile
# --------------------------------------------------------------------
# Usage examples:
#   make test            # run pytest + coverage
#   make lint            # ruff + mypy
#   make dev             # hot-reload FastAPI (local)
#   make build           # build Docker image
#   make helm-up         # upgrade Helm release (local Kube context)
#   make tf-plan         # terraform plan   (infra/terraform)
#   make tf-apply        # terraform apply  (infra/terraform)
#   make cpp-build       # compile C++ cosine-similarity library
#   make java-build      # compile Java planner JAR via Maven
#   make build-native    # compile both C++ and Java artifacts
# --------------------------------------------------------------------

PYTHON      ?= python
POETRY      ?= poetry
IMAGE_TAG   ?= agentic-ai:latest
HELM_NAME   ?= agentic-ai
HELM_CHART  ?= infra/helm/agentic-ai-assistant
KUBE_NS     ?= default
TERRAFORM_DIR = infra/terraform

# --------------------------------------------------------------------
# Python targets
# --------------------------------------------------------------------
.PHONY: test
test:
	coverage run -m pytest
	coverage report -m

.PHONY: lint
lint:
	$(PYTHON) -m pip install --quiet ruff mypy
	ruff agent api src tests
	mypy agent api src --ignore-missing-imports

.PHONY: dev
dev:
	uvicorn api.main:app --reload --port 8000

# --------------------------------------------------------------------
# Native build targets
# --------------------------------------------------------------------
.PHONY: cpp-build
cpp-build:
	g++ -O3 -shared -std=c++17 -fPIC agent/cpp/vector.cpp -o agent/cpp/libvector.so
	@echo "✓  agent/cpp/libvector.so built"

.PHONY: java-build
java-build:
	cd java && mvn package -q
	@echo "✓  agent/java/planner.jar built"

.PHONY: build-native
build-native: cpp-build java-build
	@echo "✓  All native artifacts built"

# --------------------------------------------------------------------
# Docker targets
# --------------------------------------------------------------------
.PHONY: build
build:
	docker build -t $(IMAGE_TAG) .

.PHONY: run
run:
	docker run -p 8000:8000 $(IMAGE_TAG)

# --------------------------------------------------------------------
# Helm targets
# --------------------------------------------------------------------
.PHONY: helm-up
helm-up:
	helm upgrade --install $(HELM_NAME) $(HELM_CHART) \
		--namespace $(KUBE_NS) --create-namespace

.PHONY: helm-uninstall
helm-uninstall:
	helm uninstall $(HELM_NAME) --namespace $(KUBE_NS)

# --------------------------------------------------------------------
# Terraform targets
# --------------------------------------------------------------------
.PHONY: tf-init
tf-init:
	cd $(TERRAFORM_DIR) && terraform init

.PHONY: tf-plan
tf-plan:
	cd $(TERRAFORM_DIR) && terraform plan

.PHONY: tf-apply
tf-apply:
	cd $(TERRAFORM_DIR) && terraform apply

.PHONY: tf-destroy
tf-destroy:
	cd $(TERRAFORM_DIR) && terraform destroy
