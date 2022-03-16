// Set Profile and Region from variables
provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
}

// Terraform Version
terraform {
  required_version = ">= 0.13"
}

// Tag all resources
locals {
  env  = var.environment
  tags = merge(tomap( {Environment = local.env}), var.aws_tags)
}

module "rds" {
  # source = "git@github.com:PresencePG/presence-devops-module-rds.git?ref=0.1.3"
  source = "git@github.com:slacgismo/openfido-deploy-modules.git?ref=vendor/presencepg-rds-0.1.3"
  environment       = local.env
  client            = var.client
  db_engine         = var.db_engine
  db_engine_version = var.db_engine_version
  db_name           = var.db_name
  db_user           = var.db_user
  db_port           = var.db_port
  vpc_id            = var.vpc_id
  vpc_subnet_group  = var.vpc_db_subnet_group
}