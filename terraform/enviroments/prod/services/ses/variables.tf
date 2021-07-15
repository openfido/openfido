// MakeFile variable
variable "environment" { type = string }

// Common variables
variable "aws_profile" { type = string }
variable "aws_region" { type = string }
variable "client" { type = string }
variable "aws_tags" { type = map(string) }

// SES Variables
variable "s3_bucket_prefix" {
  description = "Prefix for the S3 Bucket. Default emails"
  type        = string
  default     = "emails"
}
variable "sender_email_prefix" {
  description = "Email prefix that will be expose to the world and forward to recipient (the domain is add it base on domain variable)."
  type        = string
}
variable "recipient_email" {
  description = "The Email to forward all the senders emails."
  type        = string
}

// Inherit from vpn module
variable "domain" { type = string }
