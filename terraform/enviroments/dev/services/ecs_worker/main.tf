// Set Profile and Region from variables
provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

// Terraform Version
terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.11.0"
    }
  }
}

// Tag all resources
locals {
  env  = var.environment
  tags = merge(map("Environment", local.env), var.aws_tags)
}
