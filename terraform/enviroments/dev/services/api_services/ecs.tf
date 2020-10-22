module "ecs" {
  source = "../../../../../../../Presence/tf-module-ecs"

  environment        = local.env
  tags               = local.tags
  client             = var.stack_name
  ecr_image_name     = aws_ecr_repository.ecr[0].name
  ecr_image_tag      = var.ecs_containers[0].img_tag
  container_name     = var.ecs_containers[0].name
  container_port     = var.ecs_containers[0].port
  enable_lb          = var.ecs_containers[0].enable_lb
  vpc_id             = var.vpc_id
  vpc_public_subnets = var.vpc_public_subnets

  container_cpu = 2048
  container_memory = 4096

  tg_healthy_check_path = var.ecs_containers[0].health_check_path

  container_env_variables = {
    S3_ENDPOINT_URL: var.s3_blob_url
    FLASK_APP: "run.py"
    FLASK_ENV: "production"
    SECRET_KEY: random_password.secret.result
    SQLALCHEMY_DATABASE_URI: "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${var.db_name}"
    EMAIL_DRIVER: "sendgrid"
    SYSTEM_FROM_EMAIL_ADDRESS: "kevin.rohling@presencepg.com"
    CLIENT_BASE_URL: var.cf_domain
    // TODO: Change SendGrid variables to secrets
    SENDGRID_API_KEY: "xx"
    SENDGRID_PASSWORD_RESET_TEMPLATE_ID: "xx"
    SENDGRID_ORGANIZATION_INVITATION_TEMPLATE_ID: "xx"
  }

  depends_on = [
    aws_ecr_repository.ecr,
    aws_ecr_repository.rabbitMQ
  ]
}

//module "child_ecs" {
//  count = length(var.ecs_containers) - 1
//
//  source = "../../../../../../../Presence/tf-module-ecs"
//
//  environment = local.env
//  tags        = local.tags
//  client      = var.stack_name
//
//  ecr_image_name = aws_ecr_repository.ecr[count.index + 1].name
//  ecr_image_tag  = var.ecs_containers[count.index + 1].img_tag
//  container_name = var.ecs_containers[count.index + 1].name
//  container_port = var.ecs_containers[count.index + 1].port
//  enable_lb      = var.ecs_containers[count.index + 1].enable_lb
//
//  container_cpu = 1024
//  container_memory = 2048
//
//  tg_healthy_check_path = var.ecs_containers[0].health_check_path
//
//  ecs_cluster = {
//    id   = module.ecs.ecs_cluster_id
//    name = module.ecs.ecs_cluster_name
//  }
//
//  container_env_variables = {
//    S3_ENDPOINT_URL: var.s3_blob_url
//    FLASK_APP: "run.py"
//    FLASK_ENV: "production"
//    SECRET_KEY: random_password.secret.result
//    SQLALCHEMY_DATABASE_URI: "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${var.db_name}"
//    EMAIL_DRIVER: "sendgrid"
//    SYSTEM_FROM_EMAIL_ADDRESS: "kevin.rohling@presencepg.com"
//    CLIENT_BASE_URL: var.cf_domain
//    // TODO: Change SendGrid variables to secrets
//    SENDGRID_API_KEY: "xx"
//    SENDGRID_PASSWORD_RESET_TEMPLATE_ID: "xx"
//    SENDGRID_ORGANIZATION_INVITATION_TEMPLATE_ID: "xx"
//  }
//
//  vpc_id             = var.vpc_id
//  vpc_public_subnets = var.vpc_public_subnets
//
//  depends_on = [
//    module.ecs
//  ]
//}
//
//module "rabbitMq" {
//  source = "../../../../../../../Presence/tf-module-ecs"
//
//  environment = local.env
//  tags        = local.tags
//  client      = var.stack_name
//
//  ecr_image_name = aws_ecr_repository.rabbitMQ.name
//  ecr_image_tag  = "add-ecr"
//  container_name = "rabbitmq"
//  container_port = 5000
//  enable_lb      = false
//
//  container_cpu = 1024
//  container_memory = 2048
//
//  container_env_variables = {
//    RABBITMQ_DEFAULT_USER: "rabbit-user"
//    RABBITMQ_DEFAULT_PASS: "rabbit-password"
//    RABBITMQ_DEFAULT_VHOST: "api-queue"
//  }
//
//  ecs_cluster = {
//    id   = module.ecs.ecs_cluster_id
//    name = module.ecs.ecs_cluster_name
//  }
//
//  vpc_id             = var.vpc_id
//  vpc_public_subnets = var.vpc_public_subnets
//
//  depends_on = [
//    module.ecs
//  ]
//}
