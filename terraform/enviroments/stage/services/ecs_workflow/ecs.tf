module "ecs" {
  # source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=2.1.1"
  source = "git::https://github.com/slacgismo/openfido-deploy-modules.git?ref=vendor/presencepg-ecs-2.1.1"
  client      = var.client
  environment = local.env
  tags        = local.tags
  lb_enable   = false
  sd_enable   = true
  sd_namespace = var.sd_namespace

  container_task_definition = [{
    name           = var.ecs_name
    privileged     = false
    image          = aws_ecr_repository.ecr.name
    image_tag      = var.image_tag
    port           = var.ecs_port

    environment_variables = {
      CELERY_BROKER_URL       = var.rabbitmq_url
      CLIENT_BASE_URL         = var.cf_domain
      FLASK_APP               = "run.py"
      FLASK_ENV               = "production"
      S3_BUCKET               = var.s3_blob_name
      S3_PRESIGNED_TIMEOUT    = 3600
      SECRET_KEY              = var.secret_key
      SQLALCHEMY_DATABASE_URI = "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${var.ecs_name}service"
    }

    secrets = {}
    ssm     = {}
  }]

  containers_cpu        = 2048
  containers_memory     = 4096
  sg_list               = [var.db_sg_id, var.rabbitmq_sg_id]
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
