module "ecs" {
  source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=2.0.0"

  client      = var.client
  environment = local.env
  tags        = local.tags
  lb_enable   = true

  container_task_definition = [{
    name       = var.ecs_name
    privileged = false
    image      = aws_ecr_repository.ecr.name
    image_tag  = var.image_tag
    port       = var.ecs_port

    environment_variables = {
      AUTH_HOSTNAME           = var.auth_domain
      CLIENT_BASE_URL         = var.cf_domain
      FLASK_APP               = "run.py"
      FLASK_ENV               = "production"
      S3_ENDPOINT_URL         = var.s3_blob_url
      SECRET_KEY              = var.secret_key
      SQLALCHEMY_DATABASE_URI = "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${var.ecs_name}service"
      WORKFLOW_HOSTNAME       = var.workflow_url
      WORKFLOW_API_TOKEN      = "xx"
    }

    secrets = {}
    ssm     = {}
  }]

  containers_cpu        = 1024
  containers_memory     = 2048
  sg_list               = [var.db_sg_id, var.workflow_sg_id]
  tg_healthy_check_path = var.ecs_health_check_path

  ecs_cluster = {
    id   = var.ecs_cluster_id
    name = var.ecs_cluster_name
  }

  task_role_enable = true
  task_role_policy = [{
    sid       = "fullS3"
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = [
      var.s3_blob_arn,
      "${var.s3_blob_arn}/*"
    ]
  }]

  vpc_id              = var.vpc_id
  vpc_public_subnets  = var.vpc_public_subnets
  vpc_private_subnets = var.vpc_private_subnets
}
