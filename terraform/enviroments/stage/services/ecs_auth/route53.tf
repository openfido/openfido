resource "aws_route53_record" "auth_subdomain" {
  provider = aws.dns

  zone_id = var.auth_subdomain[local.env].zone_id
  name    = var.auth_subdomain[local.env].subdomain
  type    = "A"

  alias {
    name                   = module.ecs.lb_dns_name
    zone_id                = module.ecs.lb_zone_id
    evaluate_target_health = false
  }
}