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
      version = "~> 3"
    }
  }
}

// Tag all resources
locals {
  env  = var.environment
  tags = merge(tomap({ Environment = local.env}), var.aws_tags)
}

module "ses-forwarding" {
  source = "../../../../../../../Presence/tf-module-ses"

  client      = var.client
  environment = local.env
  tags        = local.tags

  domain           = var.domain
  mail_sender      = "${var.sender_email_prefix}@${var.domain}"
  mail_recipient   = var.recipient_email
}
