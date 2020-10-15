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

// Create VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.57.0"

  name = "${var.stack_name}-${local.env}"
  cidr = "10.12.0.0/16"

  azs             = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = ["10.12.1.0/24", "10.12.2.0/24"]
  public_subnets  = ["10.12.101.0/24", "10.12.102.0/24"]

  enable_ipv6          = true
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  // // VPC endpoint for S3
  // enable_s3_endpoint = true

  // // VPC endpoint for DynamoDB
  // enable_dynamodb_endpoint = true

  tags = local.tags
}