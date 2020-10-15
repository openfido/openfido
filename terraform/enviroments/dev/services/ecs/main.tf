// Set Profile and Region from variables
provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

// Terraform Version
terraform {
  required_version = ">= 0.12"
  required_providers {
    aws  = "~> 3.6"
    null = "~> 2.1"
  }
}

// Tag all resources
locals {
  env  = var.environment
  tags = merge(map("Environment", local.env), var.aws_tags)
}

module "ecs" {
  source = "../../../../../../../Presence/tf-module-ecs"

  client                  = var.stack_name
  environment             = local.env
  ecr_image_name          = "nginx"
  vpc_id                  = var.vpc_id
  enable_code_deploy      = true
  container_port          = 3000
  container_name          = "nginx"
  vpc_public_subnets      = var.vpc_public_subnets
  container_env_variables = {
    "CONTENTFUL_SPACE_ID"     = "vyrva4ea3218"
    "CONTENTFUL_ENVIRONMENT"  = "master"
    "CONTENTFUL_ACCESS_TOKEN" = "6Lc96L08v-7aZhhgVJQCcYyUFs7HYit2w_hDRahWZkY"
  }
}