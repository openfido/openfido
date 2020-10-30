# o = Option
# c = command

## ********** General Variables ********** #
arg1 := $(word 1,$(MAKECMDGOALS))

export TF_VAR_environment=$(arg1)

## ********** Environments where it can run ********** #
dev stage prod:
	@echo $<

## ********** Modules that can run ********** #

# ********** plan-all environment ********** #
plan:
	@echo "Running plan-all on $(arg1)"
	cd enviroments/$(arg1)/; terragrunt plan-all

# ********** apply-all environment ********** #
apply:
	@echo "Running apply-all on $(arg1)"
	cd enviroments/$(arg1)/; terragrunt apply-all

# ********** destroy-all environment ********** #
destroy:
	@echo "Running destroy-all on $(arg1)"
	cd enviroments/$(arg1)/; terragrunt destroy-all

# ********** vpc ********** #
vpc:
	@echo "Running "$c" on $(arg1) vpc"
	cd enviroments/$(arg1)/vpc/; terragrunt $c

# ******************** Data Store ******************** #
# ********** rds ********** #
rds:
	@echo "Running "$c" on $(arg1) RDS"
	cd enviroments/$(arg1)/data-storage/postgreSQL/; terragrunt $c

# ******************** Services ******************** #
# ********** Apply All Services ********** #
service-apply:
	@echo "Running Apply on $(arg1) Services"
	cd enviroments/$(arg1)/services/; terragrunt apply-all

# ********** front-end ********** #
front:
	@echo "Running "$c" on $(arg1) Front-End"
	cd enviroments/$(arg1)/services/front_end/; terragrunt $c

# ********** ecs auth ********** #
auth:
	@echo "Running "$c" on $(arg1) Auth Services"
	cd enviroments/$(arg1)/services/ecs_auth/; terragrunt $c

# ********** ecs rabbitmq ********** #
mq:
	@echo "Running "$c" on $(arg1) RabbitMQ Services"
	cd enviroments/$(arg1)/services/ecs_rabbitmq/; terragrunt $c

# ********** ecs workflow ********** #
workflow:
	@echo "Running "$c" on $(arg1) Workflow Services"
	cd enviroments/$(arg1)/services/ecs_workflow/; terragrunt $c

# ********** ecs worker ********** #
worker:
	@echo "Running "$c" on $(arg1) Worker Services"
	cd enviroments/$(arg1)/services/ecs_worker/; terragrunt $c

# ********** ecs app ********** #
app:
	@echo "Running "$c" on $(arg1) ECS App"
	cd enviroments/$(arg1)/services/ecs_app/; terragrunt $c
