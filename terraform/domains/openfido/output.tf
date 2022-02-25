output "main_domain" {
  value = var.domain
}

output "zone_id" {
  value = aws_route53_zone.host.zone_id
}

output "front_subdomain" {
  value = {
    prod = {
      zone_id   = aws_route53_zone.host.zone_id
      subdomain = local.prod_subdomain[0]
      acm_arn   = aws_acm_certificate_validation.prod_acm.certificate_arn
    }
    stage = {
      zone_id   = aws_route53_zone.host.zone_id
      subdomain = local.stage_subdomain[0]
      acm_arn   = aws_acm_certificate_validation.stage_acm.certificate_arn
    }
  }
}

output "auth_subdomain" {
  value = {
    prod = {
      zone_id   = aws_route53_zone.host.zone_id
      subdomain = local.prod_subdomain[1]
      acm_arn   = aws_acm_certificate_validation.prod_acm.certificate_arn
    }
    stage = {
      zone_id   = aws_route53_zone.host.zone_id
      subdomain = local.stage_subdomain[1]
      acm_arn   = aws_acm_certificate_validation.stage_acm.certificate_arn
    }
  }
}

output "app_subdomain" {
  value = {
    prod = {
      zone_id   = aws_route53_zone.host.zone_id
      subdomain = local.prod_subdomain[2]
      acm_arn   = aws_acm_certificate_validation.prod_acm.certificate_arn
    }
    stage = {
      zone_id   = aws_route53_zone.host.zone_id
      subdomain = local.stage_subdomain[2]
      acm_arn   = aws_acm_certificate_validation.stage_acm.certificate_arn
    }
  }
}
