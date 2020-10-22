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
  tags = merge(map("Environment", local.env), var.aws_tags)
}

// Create VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.57.0"

  name = "${var.stack_name}-${local.env}"
  cidr = "10.12.0.0/16"

  azs              = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets  = ["10.12.1.0/24", "10.12.2.0/24"]
  database_subnets = ["10.12.50.0/24", "10.12.51.0/24"]
  public_subnets   = ["10.12.101.0/24", "10.12.102.0/24"]

  // Options for the subnets
  enable_ipv6          = false
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  // VPC endpoint for S3
  enable_s3_endpoint = true

  // DB Subnet options
  create_database_subnet_route_table = true

  tags = local.tags
}