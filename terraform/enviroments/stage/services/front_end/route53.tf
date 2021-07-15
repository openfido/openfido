resource "aws_route53_record" "cf_subdomain" {
  provider = aws.dns

  zone_id = var.front_subdomain[local.env].zone_id
  name    = var.front_subdomain[local.env].subdomain
  type    = "A"

  alias {
    name                   = module.cf.cloudfront_distribution_domain_name
    zone_id                = module.cf.cloudfront_distribution_hosted_zone_id
    evaluate_target_health = false
  }
}