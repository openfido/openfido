// Configure Terragrunt to automatically store tfstate files in an S3 bucket
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config  = {
    bucket         = "openfido-remote-state"
    dynamodb_table = "openfido-remote-state-lock"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    profile        = "openfido"
    encrypt        = true
  }
}