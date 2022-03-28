// Set Profile and Region from variables
provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

provider "aws" {
  alias   = "stage"
  profile = "openfido-stage"
  region  = var.aws_region
}

// Terraform Version
terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3"
    }
  }
}

// Tag all resources
locals {
  env             = var.environment
  tags            = merge(tomap({ Environment = local.env }), var.aws_tags)
  prod_subdomain  = [for sub in var.prod_subdomains : "${sub}.${var.domain}"]
  stage_subdomain = [for sub in var.stage_subdomains : "${sub}.${var.domain}"]
}
