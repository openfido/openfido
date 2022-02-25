variable "prefix" {
  default = "openfido"
}

variable "project" {
  default = "openfido"
}

variable "contact" {
  default = "jimmyleu@slac.stanford.edu"
}


# database

variable "db_user" {
  description = "Username for the RDS Postgres instance"
  default     = "openfido"
}

variable "db_password" {
  description = "Password for the RDS postgres instance"
}

variable "db_engine" {
  description = "database engine "
  default     = "postgres"
}

variable "db_engine_version" {
  description = "database version "
  default     = "11.8"
}

variable "db_name" {
  description = "database name"
  default     = "appservice"
}

variable "db_port" {
  description = "database port"
  default     = 5432
}

variable "db_class" {
  description = "database class"
  default     = "db.t3.small"
}

