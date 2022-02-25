// Set Profile and Region from variables
provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

provider "aws" {
  alias   = "dns"
  profile = "openfido-prod"
  region  = var.aws_region
}

// Terraform Version
terraform {
  required_version = ">= 0.13"
  required_providers {
    aws    = {
      source  = "hashicorp/aws"
      version = "~> 3"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3"
    }
  }
}

resource "random_password" "secret" {
  length           = 20
  special          = true
  override_special = "!#$%^&*()-_=+[]{}<>:?"
  keepers          = {
    pass_version = 1
  }
}

// Tag all resources
locals {
  env  = var.environment
  tags = merge(tomap({Environment = local.env}), var.aws_tags)
}
