resource "aws_s3_bucket" "website" {
  bucket = local.s3_website
  acl    = "public-read"
  policy = data.aws_iam_policy_document.s3_website.json

  website {
    index_document = "index.html"
    # error_document = "index.html"
  }

  tags = merge(map(
  "Name", local.s3_website
  ), local.tags)
}

data "aws_iam_policy_document" "s3_website" {
  statement {
    sid       = "AllowS3GetObject"
    effect    = "Allow"
    principals {
      identifiers = ["*"]
      type        = "*"
    }
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${local.s3_website}/*"]
  }
}

resource "aws_s3_bucket" "blob" {
  bucket = local.s3_blob
  acl    = "private"

  tags = merge(map(
    "Name", local.s3_blob
  ), local.tags)
}
