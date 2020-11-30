// App Service
module "ecs" {
  source = "git@github.com:PresencePG/presence-devops-module-ecs.git?ref=2.1.1"

  client      = var.client
  environment = local.env
  tags        = local.tags

  lb_enable       = true
  lb_acm_arn      = var.auth_subdomain[local.env].acm_arn
  lb_enable_https = true

  container_task_definition = [
    {
      name       = var.ecs_name
      privileged = false
      image      = aws_ecr_repository.ecr.name
      image_tag  = var.image_tag
      port       = var.ecs_port

      environment_variables = {
        CLIENT_BASE_URL                              = var.cf_domain
        EMAIL_DRIVER                                 = "sendgrid"
        FLASK_APP                                    = "run.py"
        FLASK_ENV                                    = "production"
        S3_BUCKET                                    = var.s3_blob_name
        S3_PRESIGNED_TIMEOUT                         = 3600
        SECRET_KEY                                   = random_password.secret.result
        SQLALCHEMY_DATABASE_URI                      = "postgresql://${var.db_user}:${var.db_password}@${var.db_endpoint}/${var.ecs_name}service"
        SYSTEM_FROM_EMAIL_ADDRESS                    = "support@openfido.org"
        // TODO: Change to secrets, for this they should be read it as JSON
        SENDGRID_API_KEY                             = "xx"
        SENDGRID_PASSWORD_RESET_TEMPLATE_ID          = "xx"
        SENDGRID_ORGANIZATION_INVITATION_TEMPLATE_ID = "xx"
      }

      secrets = {}
      ssm     = {}
    }]

  sg_list               = [var.db_sg_id]
  tg_healthy_check_path = var.ecs_health_check_path

  task_role_enable = true
  task_role_policy = [
    {
      sid       = "fullS3"
      effect    = "Allow"
      actions   = [
        "s3:*"]
      resources = [
        var.s3_blob_arn,
        "${var.s3_blob_arn}/*"
      ]
    }
  ]

  vpc_id              = var.vpc_id
  vpc_public_subnets  = var.vpc_public_subnets
  vpc_private_subnets = var.vpc_private_subnets
}
