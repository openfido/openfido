module "cf" {
  source = "git@github.com:PresencePG/presence-devops-module-cloudfront.git?ref=0.1.0"

  environment         = local.env
  tags                = local.tags
  client              = var.client
  is_ipv6_enabled     = true
  price_class         = "PriceClass_100"
  retain_on_delete    = false
  wait_for_deployment = false
  aliases             = [var.front_subdomain[local.env].subdomain]

  # Create Permissions for s3 static
  create_origin_access_identity = true
  origin_access_identities      = {
    static_s3 = "S3 Bucket for the front end"
  }

  origin = {
    # S3 Website
    s3_front = {
      domain_name          = aws_s3_bucket.website.website_endpoint
      custom_origin_config = {
        http_port              = 80
        https_port             = 443
        origin_protocol_policy = "http-only"
        origin_ssl_protocols   = ["TLSv1.2"]
      }
    }
    # Static S3 content
    static_s3 = {
      domain_name = aws_s3_bucket.website.bucket_domain_name
      s3_origin_config     = {
        origin_access_identity = "static_s3"
      }
    }
  }

  cache_behavior = {
    # S3 Website
    default = {
      target_origin_id       = "s3_front"
      viewer_protocol_policy = "redirect-to-https"

      allowed_methods = ["GET", "HEAD", "OPTIONS"]
      cached_methods  = ["GET", "HEAD"]
      compress        = true
      query_string    = true

      cookies_forward = "all"
    }
    # Static S3 content
    s3 = {
      path_pattern           = "/static/*"
      target_origin_id       = "static_s3"
      viewer_protocol_policy = "redirect-to-https"

      allowed_methods = ["GET", "HEAD", "OPTIONS"]
      cached_methods  = ["GET", "HEAD"]
      compress        = true
      query_string    = true
    }
  }

  viewer_certificate = {
    acm_certificate_arn      = var.front_subdomain[local.env].acm_arn
    minimum_protocol_version = "TLSv1.2_2019"
    ssl_support_method       = "sni-only"
  }

  custom_error_response = {
    not_found = {
      error_caching_min_ttl = 10
      error_code            = 404
      response_code         = 200
      response_page_path    = "/"
    }
  }
}