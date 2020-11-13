// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "client" { type = string }
variable "aws_tags" { type = map(string) }

// Domain Certificate ARN
variable "front_subdomain" {
  type = map(object({
    zone_id   = string
    subdomain = string
    acm_arn   = string
  }))
}
