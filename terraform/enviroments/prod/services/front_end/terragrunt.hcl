include {
  path = find_in_parent_folders()
}

terraform {
  extra_arguments "common_vars" {
    commands = get_terraform_commands_that_need_vars()

    arguments = [
      "-var-file=${get_parent_terragrunt_dir()}/variables/common.tfvars"
    ]
  }
}

// Dependency's for this terraform
dependency "domain_openfido" {
  config_path = "../../../../domains/openfido"
}

// Input values
inputs = {
  front_subdomain = dependency.domain_openfido.outputs.front_subdomain
}