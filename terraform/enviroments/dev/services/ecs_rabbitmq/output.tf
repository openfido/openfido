output "sd_domain" {
  value = module.ecs.sd_domain
}

output "sd_namespace" {
  value = module.ecs.sd_namespace
}

output "rabbitmq_sg_id" {
  value = module.ecs.sg_id
}

output "rabbitmq_url" {
  value = "amqp://rabbit-user:rabbit-password@${module.ecs.sd_name}.${module.ecs.sd_domain}/api-queue"
}
