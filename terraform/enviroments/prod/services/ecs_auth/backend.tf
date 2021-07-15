# Generated by Terragrunt. Sig: nIlQXj57tbuaRZEa
terraform {
  backend "s3" {
    dynamodb_table = "openfido-remote-state-lock"
    encrypt        = true
    key            = "enviroments/prod/services/ecs_auth/terraform.tfstate"
    profile        = "openfido-stage"
    region         = "us-east-1"
    bucket         = "openfido-remote-state"
  }
}
