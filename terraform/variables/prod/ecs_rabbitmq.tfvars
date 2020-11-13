ecs_name              = "rabbitmq"
image_tag             = "master"
ecs_health_check_path = "/healthcheck"
ecs_port              = 5672

rabbitmq_pass  = "rabbit-password"
rabbitmq_user  = "rabbit-user"
rabbitmq_vhost = "api-queue"