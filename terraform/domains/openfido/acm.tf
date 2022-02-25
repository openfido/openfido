// Prod Certificates
resource "aws_acm_certificate" "prod_acm" {
  domain_name               = local.prod_subdomain[0]
  subject_alternative_names = slice(local.prod_subdomain, 1, length(local.prod_subdomain))
  validation_method         = "DNS"

  tags = merge(tomap(
    { Name = "Prod Subdomains ${var.domain}" }
  ), local.tags)
}

resource "aws_route53_record" "prod_acm" {
  for_each = {
    for dvo in aws_acm_certificate.prod_acm.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = aws_route53_zone.host.zone_id
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = each.value.zone_id
}

resource "aws_acm_certificate_validation" "prod_acm" {
  certificate_arn         = aws_acm_certificate.prod_acm.arn
  validation_record_fqdns = [for record in aws_route53_record.prod_acm : record.fqdn]
}

// Stage certificates
resource "aws_acm_certificate" "stage_acm" {
  provider = aws.stage

  domain_name               = local.stage_subdomain[0]
  subject_alternative_names = slice(local.stage_subdomain, 1, length(local.stage_subdomain))
  validation_method         = "DNS"

  tags = merge(tomap(
    { Name = "Stage Subdomains ${var.domain}" }
  ), local.tags)
}

resource "aws_acm_certificate_validation" "stage_acm" {
  provider = aws.stage

  certificate_arn         = aws_acm_certificate.stage_acm.arn
  validation_record_fqdns = [for record in aws_route53_record.stage_acm : record.fqdn]
}

resource "aws_route53_record" "stage_acm" {
  for_each = {
    for dvo in aws_acm_certificate.stage_acm.domain_validation_options : dvo.domain_name => {
      name    = dvo.resource_record_name
      record  = dvo.resource_record_value
      type    = dvo.resource_record_type
      zone_id = aws_route53_zone.host.zone_id
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = each.value.zone_id
}
