###############################################################################
# Terraform – Agentic AI Assistant (EKS + Helm)
###############################################################################

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws   = { source = "hashicorp/aws",   version = "~> 5.47" }
    helm  = { source = "hashicorp/helm",  version = "~> 2.13" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.29" }
  }
}

# ---------------------------------------------------------------------------
# 1. AWS provider
# ---------------------------------------------------------------------------
provider "aws" {
  region = var.aws_region
}

# ---------------------------------------------------------------------------
# 2. EKS cluster (terraform-aws-modules)
# ---------------------------------------------------------------------------
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.13.0"

  cluster_name    = "agentic-ai-eks"
  cluster_version = "1.29"
  vpc_id          = var.vpc_id
  subnet_ids      = var.public_subnet_ids

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]
      desired_capacity = 2
      min_capacity     = 1
      max_capacity     = 3
    }
  }
}

# ---------------------------------------------------------------------------
# 3. Helm provider (uses EKS kubeconfig)
# ---------------------------------------------------------------------------
provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    token                  = module.eks.cluster_token
  }
}

# ---------------------------------------------------------------------------
# 4. Helm release – Agentic AI Assistant
# ---------------------------------------------------------------------------
resource "helm_release" "agentic_ai" {
  name       = "agentic-ai"
  chart      = "${path.module}/../helm/agentic-ai-assistant"
  namespace  = "default"
  create_namespace = true

  values = [
    file("${path.module}/../helm/agentic-ai-assistant/values.yaml")
  ]
}

# ---------------------------------------------------------------------------
# 5. Outputs
# ---------------------------------------------------------------------------
output "cluster_name" {
  value = module.eks.cluster_name
}

output "kubeconfig" {
  value = module.eks.kubeconfig
  sensitive = true
}

###############################################################################
# Variables (adjust to your AWS environment)
###############################################################################
variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs for EKS worker nodes"
  type        = list(string)
}
