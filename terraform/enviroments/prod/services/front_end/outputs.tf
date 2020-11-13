output "s3_blob_name" {
  value = aws_s3_bucket.blob.bucket
}

output "s3_blob_arn" {
  value = aws_s3_bucket.blob.arn
}

output "s3_blob_url" {
  value = aws_s3_bucket.blob.bucket_regional_domain_name
}

output "cf_domain" {
  value = var.front_subdomain[local.env].subdomain
}