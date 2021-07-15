resource "aws_route53_zone" "host" {
  name = var.domain
  tags = local.tags
}

//resource "aws_route53_record" "main" {
//  name    = aws_route53_zone.host.name
//  zone_id = aws_route53_zone.host.zone_id
//  type    = "A"
//  alias {
//    name                   = aws_s3_bucket.website.website_domain
//    zone_id                = aws_s3_bucket.website.hosted_zone_id
//    evaluate_target_health = true
//  }
//}

resource "aws_route53_record" "www_main" {
  name    = "www.${aws_route53_zone.host.name}"
  zone_id = aws_route53_zone.host.zone_id
  type    = "A"
  alias {
    name                   = aws_s3_bucket.www_website.website_domain
    zone_id                = aws_s3_bucket.www_website.hosted_zone_id
    evaluate_target_health = true
  }
}
