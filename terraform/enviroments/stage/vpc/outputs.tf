output "vpc_id" {
  description = "VPC ID"
  value = module.vpc.vpc_id
}

output "vpc_default_sg" {
  description = "Default Security Group for VPC"
  value = module.vpc.default_security_group_id
}

output "vpc_public_subnets" {
  description = "List of IDs of public subnets"
  value = module.vpc.public_subnets
}

output "vpc_private_subnets" {
  description = "List of IDs of private subnets"
  value = module.vpc.private_subnets
}

output "vpc_db_subnets" {
  value = module.vpc.database_subnets
}

output "vpc_db_subnet_group" {
  value = module.vpc.database_subnet_group
}