terraform {
  backend "s3" {
    bucket         = "openfido-stage-tfstate"
    key            = "openfido-stage.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "openfido-stage-tf-state-lock"
  }
}

provider "aws" {
  region = "us-east-1"
}

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
}

