output "secret_key" {
  value = random_password.secret.result
}

output "ecs_cluster_id" {
  value = module.ecs.ecs_cluster_id
}

output "ecs_cluster_name" {
  value = module.ecs.ecs_cluster_name
}

output "auth_domain" {
  value = var.auth_subdomain[local.env].subdomain
}
