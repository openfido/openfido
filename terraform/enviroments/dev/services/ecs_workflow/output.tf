output "workflow_sg_id" {
  value = module.ecs.sg_id
}

output "workflow_url" {
  value = "http://${module.ecs.sd_name}.${var.rabbitmq_url}:${var.ecs_port}"
}
