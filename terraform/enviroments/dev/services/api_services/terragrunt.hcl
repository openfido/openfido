include {
  path = find_in_parent_folders()
}

terraform {
  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()

    arguments = [
      "-var-file=${get_parent_terragrunt_dir()}/variables/common.tfvars",
      "-var-file=${get_parent_terragrunt_dir()}/variables/${get_env("TF_VAR_environment")}/ecs.tfvars"
    ]
  }
}

// Dependency's for this terraform
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
  db_name             = dependency.rds.outputs.db_instance_name
  db_password         = dependency.rds.outputs.db_instance_password
  db_endpoint         = dependency.rds.outputs.db_instance_address
  s3_blob_url         = dependency.front.outputs.s3_blob_url
  cf_domain           = dependency.front.outputs.cf_domain
}