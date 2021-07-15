// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "client" { type = string }
variable "aws_tags" { type = map(string) }

// DB variables
variable "db_engine" { type = string }
variable "db_engine_version" { type = string }
variable "db_name" { type = string }
variable "db_user" { type = string }
variable "db_port" { type = number }

// Inherit from vpn module
variable "vpc_id" { type = string }
variable "vpc_default_sg" { type = string }
variable "vpc_public_subnets" { type = list(string) }
variable "vpc_private_subnets" { type = list(string) }
variable "vpc_db_subnets" { type = list(string) }
variable "vpc_db_subnet_group" { type = string }
