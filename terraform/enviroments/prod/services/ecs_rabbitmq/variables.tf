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
variable "rabbitmq_user" {
  description = "The rabbitmq user."
  type        = string
}
variable "rabbitmq_pass" {
  description = "The rabbitmq password."
  type        = string
}
variable "rabbitmq_vhost" {
  description = "The rabbitmq vhost."
  type        = string
}

// Inherit from vpn module
variable "vpc_id" { type = string }
variable "vpc_default_sg" { type = string }
variable "vpc_public_subnets" { type = list(string) }
variable "vpc_private_subnets" { type = list(string) }
variable "ecs_cluster_id" { type = string }
variable "ecs_cluster_name" { type = string }
