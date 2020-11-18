// Configure Terragrunt to automatically store tfstate files in an S3 bucket
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config  = {
    bucket         = "openfido-remote-state"
    dynamodb_table = "openfido-remote-state-lock"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = get_env("TF_VAR_aws_region")
    profile        = "openfido-stage"
    encrypt        = true
  }
}