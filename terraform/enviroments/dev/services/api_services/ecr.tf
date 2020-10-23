resource "aws_ecr_repository" "rabbitMQ" {
  name                 = "${var.stack_name}/${var.environment}-rabbitmq"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "ecr" {
  count = length(local.list_ecs_name)

  name                 = "${var.stack_name}/${var.environment}-${local.list_ecs_name[count.index]}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
