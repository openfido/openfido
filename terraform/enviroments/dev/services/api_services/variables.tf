// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "stack_name" { type = string }
variable "aws_tags" { type = map(string) }

// ECS Variables
variable "ecs_containers" {
  description = "The containers to create."

  type = list(object({
    name              = string
    port              = number
    img_tag           = string
    enable_lb         = bool
    health_check_path = string
  }))
}

// Inherit from vpn module
variable "vpc_id" { type = string }
variable "vpc_default_sg" { type = string }
variable "vpc_public_subnets" { type = list(string) }
variable "vpc_private_subnets" { type = list(string) }
variable "db_user" { type = string }
variable "db_name" { type = string }
variable "db_password" { type = string }
variable "db_endpoint" { type = string }
variable "cf_domain" { type = string }
variable "s3_blob_url" { type = string }
