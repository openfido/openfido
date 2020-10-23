ecs_containers = {
  app             = {
    port              = 5000
    img_tag           = "latest"
    enable_lb         = true
    health_check_path = "/healthcheck"
  }
  auth            = {
    port              = 5000
    img_tag           = "latest"
    enable_lb         = true
    health_check_path = "/healthcheck"
  }
  workflow        = {
    port              = 5000
    img_tag           = "latest"
    enable_lb         = true
    health_check_path = "/healthcheck"
  }
  workflow-worker = {
    port              = 5151
    img_tag           = "latest"
    enable_lb         = false
    health_check_path = null
  }
}
