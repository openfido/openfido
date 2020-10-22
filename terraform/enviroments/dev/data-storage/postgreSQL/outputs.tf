output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = module.rds.db_instance_address
}

output "db_instance_username" {
  description = "The master username for the database"
  value       = module.rds.db_instance_username
}

output "db_instance_password" {
  description = "The master password for the database"
  value       = module.rds.db_instance_password
}

output "db_instance_name" {
  description = "The master password for the database"
  value       = module.rds.db_instance_name
}

output "db_instance_port" {
  description = "The database port"
  value       = module.rds.db_instance_port
}