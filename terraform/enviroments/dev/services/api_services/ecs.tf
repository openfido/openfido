module "ecs_app" {
  source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=0.3.0"

  environment        = local.env
  tags               = local.tags
  client             = var.stack_name
  ecr_image_name     = aws_ecr_repository.ecr[index(local.list_ecs_name, "app")].name
  ecr_image_tag      = lookup(var.ecs_containers, "app").img_tag
  container_name     = local.list_ecs_name[index(local.list_ecs_name, "app")]
  container_port     = lookup(var.ecs_containers, "app").port
  enable_lb          = lookup(var.ecs_containers, "app").enable_lb
  vpc_id             = var.vpc_id
  vpc_public_subnets = var.vpc_public_subnets

  container_cpu         = 1024
  container_memory      = 2048
  sg_list               = [var.db_sg_id]
  tg_healthy_check_path = lookup(var.ecs_containers, "app").health_check_path

  container_env_variables = {
    FLASK_APP                 = "run.py"
    FLASK_ENV                 = "production"
    EMAIL_DRIVER              = "sendgrid"
    SYSTEM_FROM_EMAIL_ADDRESS = "xx.rohling@xx.com"
    S3_ENDPOINT_URL           = var.s3_blob_url
    CLIENT_BASE_URL           = var.cf_domain
    SECRET_KEY                = random_password.secret.result
    SQLALCHEMY_DATABASE_URI   = "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${local.list_ecs_name[index(local.list_ecs_name, "app")]}service"
  }
}

module "ecs_auth" {
  source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=0.3.0"

  environment = local.env
  tags        = local.tags
  client      = var.stack_name

  ecr_image_name = aws_ecr_repository.ecr[index(local.list_ecs_name, "auth")].name
  ecr_image_tag  = lookup(var.ecs_containers, "auth").img_tag
  container_name = local.list_ecs_name[index(local.list_ecs_name, "auth")]
  container_port = lookup(var.ecs_containers, "auth").port
  enable_lb      = lookup(var.ecs_containers, "auth").enable_lb

  container_cpu         = 256
  container_memory      = 512
  sg_list               = [var.db_sg_id]
  tg_healthy_check_path = lookup(var.ecs_containers, "auth").health_check_path

  ecs_cluster = {
    id   = module.ecs_app.ecs_cluster_id
    name = module.ecs_app.ecs_cluster_name
  }

  container_env_variables = {
    FLASK_APP                                    = "run.py"
    FLASK_ENV                                    = "production"
    EMAIL_DRIVER                                 = "sendgrid"
    SYSTEM_FROM_EMAIL_ADDRESS                    = "xx.xx@xx.com"
    S3_ENDPOINT_URL                              = var.s3_blob_url
    CLIENT_BASE_URL                              = var.cf_domain
    SECRET_KEY                                   = random_password.secret.result
    SQLALCHEMY_DATABASE_URI                      = "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${local.list_ecs_name[index(local.list_ecs_name, "auth")]}service"
    // TODO: Change SendGrid variables to secrets
    SENDGRID_API_KEY                             = "xx"
    SENDGRID_PASSWORD_RESET_TEMPLATE_ID          = "d-xx"
    SENDGRID_ORGANIZATION_INVITATION_TEMPLATE_ID = "d-xx"
  }

  vpc_id             = var.vpc_id
  vpc_public_subnets = var.vpc_public_subnets

  depends_on = [module.ecs_app]
}


module "ecs_workflow" {
  source = "../../../../../../../Presence/tf-module-ecs"

  environment  = local.env
  tags         = local.tags
  client       = var.stack_name
  service_name = "workflow"
  enable_lb    = lookup(var.ecs_containers, "workflow").enable_lb

  container_task_definition = [
    {
      name                  = "workflow"
      image                 = aws_ecr_repository.ecr[index(local.list_ecs_name, "workflow")].name
      image_tag             = lookup(var.ecs_containers, "workflow").img_tag
      port                  = lookup(var.ecs_containers, "workflow").port
      environment_variables = {
        FLASK_APP               = "run.py"
        FLASK_ENV               = "production"
        CELERY_BROKER_URL       = "amqp://rabbit-user:rabbit-password@rabbitmq/api-queue"
        S3_ENDPOINT_URL         = var.s3_blob_url
        CLIENT_BASE_URL         = var.cf_domain
        SECRET_KEY              = random_password.secret.result
        WORKFLOW_API_TOKEN      = "xx"
        SQLALCHEMY_DATABASE_URI = "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${local.list_ecs_name[index(local.list_ecs_name, "workflow")]}service"
      }
      secrets = {}
    },
    {
      name                  = "workflow-worker"
      image                 = aws_ecr_repository.ecr[index(local.list_ecs_name, "workflow-worker")].name
      image_tag             = lookup(var.ecs_containers, "workflow-worker").img_tag
      port                  = lookup(var.ecs_containers, "workflow-worker").port
      environment_variables = {
        FLASK_APP: "run.py"
        FLASK_ENV: "production"
        S3_ENDPOINT_URL   = var.s3_blob_url
        CLIENT_BASE_URL   = var.cf_domain
        SECRET_KEY        = random_password.secret.result
        WORKER_API_SERVER = "http://127.0.0.1:5000"
        WORKER_API_TOKEN  = "xx"
        CELERY_BROKER_URL = "amqp://xx-xx:xx-xx@127.0.0.1/api-queue"
      }
      secrets = {}
    },
    {
      name                  = "rabbitmq"
      image                 = aws_ecr_repository.rabbitMQ.name
      image_tag             = "add-ecr"
      port                  = 5672
      environment_variables = {
        RABBITMQ_DEFAULT_USER  = "xx-xx"
        RABBITMQ_DEFAULT_PASS  = "xx-xx"
        RABBITMQ_DEFAULT_VHOST = "xx-xx"
      }
      secrets = {}
    }
  ]

  containers_cpu             = 2048
  containers_memory          = 4096
  sg_list                   = [var.db_sg_id]
  tg_healthy_check_path     = lookup(var.ecs_containers, "workflow").health_check_path

  ecs_cluster = {
    id   = module.ecs_app.ecs_cluster_id
    name = module.ecs_app.ecs_cluster_name
  }

  vpc_id             = var.vpc_id
  vpc_public_subnets = var.vpc_public_subnets

  depends_on = [module.ecs_app]
}
