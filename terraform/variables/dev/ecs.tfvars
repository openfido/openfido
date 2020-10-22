ecs_containers = [
  {
    name              = "app"
    port              = 5000
    img_tag           = "latest"
    enable_lb         = true
    health_check_path = "/healthcheck"
  },
  {
    name              = "auth"
    port              = 5000
    img_tag           = "latest"
    enable_lb         = true
    health_check_path = "/healthcheck"
  },
  {
    name              = "workflow"
    port              = 5000
    img_tag           = "latest"
    enable_lb         = true
    health_check_path = "/healthcheck"
  },
  {
    name              = "workflow-worker"
    port              = 5000
    img_tag           = "latest"
    enable_lb         = false
    health_check_path = null
  }
]