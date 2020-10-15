// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "stack_name" { type = string }
variable "aws_tags" { type = map(string) }

// Get AWS Availability zones
data "aws_availability_zones" "available" {}