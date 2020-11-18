include {
  path = find_in_parent_folders()
}

terraform {
  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()

    arguments = [
      "-var-file=${get_parent_terragrunt_dir()}/variables/common.tfvars",
      "-var-file=${get_parent_terragrunt_dir()}/variables/${get_env("TF_VAR_environment")}/ecs_worker.tfvars"
    ]
  }
}

// Dependency's for this terraform
dependency "ecs_workflow" {
  config_path = "../ecs_workflow"
}

dependency "ecs_rabbitmq" {
  config_path = "../ecs_rabbitmq"
}

dependency "ecs_auth" {
  config_path = "../ecs_auth"
}

dependency "front" {
  config_path = "../front_end"
}

dependency "vpc" {
  config_path = "../../vpc"
}

dependency "rds" {
  config_path = "../../data-storage/postgreSQL"
}

// Input values
inputs = {
  vpc_id              = dependency.vpc.outputs.vpc_id
  vpc_default_sg      = dependency.vpc.outputs.vpc_default_sg
  vpc_public_subnets  = dependency.vpc.outputs.vpc_public_subnets
  vpc_private_subnets = dependency.vpc.outputs.vpc_private_subnets
  db_user             = dependency.rds.outputs.db_instance_username
  db_password         = dependency.rds.outputs.db_instance_password
  db_endpoint         = dependency.rds.outputs.db_instance_address
  db_sg_id            = dependency.rds.outputs.db_sg_id
  cf_domain           = dependency.front.outputs.cf_domain
  s3_blob_name        = dependency.front.outputs.s3_blob_name
  ecs_cluster_id      = dependency.ecs_auth.outputs.ecs_cluster_id
  ecs_cluster_name    = dependency.ecs_auth.outputs.ecs_cluster_name
  rabbitmq_url        = dependency.ecs_rabbitmq.outputs.rabbitmq_url
  rabbitmq_sg_id      = dependency.ecs_rabbitmq.outputs.rabbitmq_sg_id
  workflow_url        = dependency.ecs_workflow.outputs.workflow_url
  workflow_sg_id      = dependency.ecs_workflow.outputs.workflow_sg_id
}