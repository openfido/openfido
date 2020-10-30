module "ecs" {
  source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=2.0.0"

  client         = var.client
  environment    = local.env
  tags           = local.tags
  lb_enable      = false
  fargate_enable = false

  container_task_definition = [{
    name       = var.ecs_name
    privileged = true
    image      = aws_ecr_repository.ecr.name
    image_tag  = var.image_tag
    port       = var.ecs_port

    environment_variables = {
      CELERY_BROKER_URL = var.rabbitmq_url
      WORKER_API_SERVER = var.workflow_url
      // TODO: add to secrets
      WORKER_API_TOKEN  = "xx"
    }

    secrets = {}
    ssm     = {}
  }]

  sg_list = [var.rabbitmq_sg_id, var.workflow_sg_id]

  ecs_cluster = {
    id   = var.ecs_cluster_id
    name = var.ecs_cluster_name
  }

  vpc_id              = var.vpc_id
  vpc_public_subnets  = var.vpc_public_subnets
  vpc_private_subnets = var.vpc_private_subnets
}
