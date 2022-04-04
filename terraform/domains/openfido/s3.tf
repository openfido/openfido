resource "aws_s3_bucket" "website" {
  bucket        = var.domain
  acl           = "public-read"
  force_destroy = true

  website {
    redirect_all_requests_to = "https://github.com/slacgismo/openfido"
  }

  tags = merge(tomap(
    { Name = var.domain }
  ), local.tags)
}

resource "aws_s3_bucket" "www_website" {
  bucket        = "www.${var.domain}"
  acl           = "public-read"
  force_destroy = true

  website {
    redirect_all_requests_to = "https://github.com/slacgismo/openfido"
  }

  tags = merge(tomap(
    { Name = "www.${var.domain}" }
  ), local.tags)
}
