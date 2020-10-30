// App Service
module "ecs" {
  source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=2.0.0"

  client      = var.client
  environment = local.env
  tags        = local.tags
  lb_enable   = false
  sd_enable   = true

  container_task_definition = [
  {
    name       = var.ecs_name
    privileged = false
    image      = aws_ecr_repository.ecr.name
    image_tag  = var.image_tag
    port       = var.ecs_port

    environment_variables = {
      RABBITMQ_DEFAULT_PASS  = var.rabbitmq_pass
      RABBITMQ_DEFAULT_USER  = var.rabbitmq_user
      RABBITMQ_DEFAULT_VHOST = var.rabbitmq_vhost
    }

    secrets = {}
    ssm     = {}
  }]

  containers_cpu    = 1024
  containers_memory = 2048

  ecs_cluster = {
    id   = var.ecs_cluster_id
    name = var.ecs_cluster_name
  }

  vpc_id              = var.vpc_id
  vpc_public_subnets  = var.vpc_public_subnets
  vpc_private_subnets = var.vpc_private_subnets
}
