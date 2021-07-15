// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "aws_tags" { type = map(string) }
variable "client" { type = string }

// Domain openfido
variable "domain" { type = string }
variable "prod_subdomains" { type = list(string) }
variable "stage_subdomains" { type = list(string) }