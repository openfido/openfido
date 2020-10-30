resource "aws_ecr_repository" "ecr" {
  name                 = "${var.client}/${var.environment}-${var.ecs_name}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
