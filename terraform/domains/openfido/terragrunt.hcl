include {
  path = find_in_parent_folders()
}

terraform {
  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()

    arguments = [
      "-var-file=${get_parent_terragrunt_dir()}/variables/common.tfvars",
      "-var-file=${get_parent_terragrunt_dir()}/variables/domains/openfido.tfvars"
    ]
  }
}
