// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "stack_name" { type = string }
variable "aws_tags" { type = map(string) }

// Inherit from vpn module
variable "vpc_id" { type = string }
variable "vpc_default_sg" { type = string }
variable "vpc_public_subnets" { type = list(string) }
variable "vpc_private_subnets" { type = list(string) }
