resource "aws_ecr_repository" "rabbitMQ" {
  name                 = "${var.stack_name}/${var.environment}-rabbitmq"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "ecr" {
  count = length(var.ecs_containers)

  name                 = "${var.stack_name}/${var.environment}-${var.ecs_containers[count.index].name}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
