// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "client" { type = string }
variable "aws_tags" { type = map(string) }

// ECS Variables
variable "ecs_name" {
  description = "The containers name."
  type        = string
}
variable "ecs_port" {
  description = "The containers port."
  type        = string
}
variable "image_tag" {
  description = "The containers image tag."
  type        = string
}
variable "ecs_health_check_path" {
  description = "The containers health check path."
  type        = string
}

// Inherit from vpn module
variable "vpc_id" { type = string }
variable "vpc_default_sg" { type = string }
variable "vpc_public_subnets" { type = list(string) }
variable "vpc_private_subnets" { type = list(string) }
variable "db_user" { type = string }
variable "db_password" { type = string }
variable "db_endpoint" { type = string }
variable "db_sg_id" { type = string }
variable "cf_domain" { type = string }
variable "s3_blob_name" { type = string }
variable "s3_blob_arn" { type = string }
variable "ecs_cluster_id" { type = string }
variable "ecs_cluster_name" { type = string }
variable "secret_key" { type = string }
variable "rabbitmq_url" { type = string }
variable "rabbitmq_sg_id" { type = string }
variable "sd_domain" { type = string }
variable "sd_namespace" { type = string }
