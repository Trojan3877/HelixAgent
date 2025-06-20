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
	ruff agent app tests
	mypy agent app --ignore-missing-imports

.PHONY: dev
dev:
	uvicorn app.api:app --reload --port 8000

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
