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

# ********** ecs ********** #
api:
	@echo "Running "$c" on $(arg1) Api Services"
	cd enviroments/$(arg1)/services/api_services/; terragrunt $c

# ********** front-end ********** #
front:
	@echo "Running "$c" on $(arg1) Front-End"
	cd enviroments/$(arg1)/services/front_end/; terragrunt $c

# ********** rds ********** #
rds:
	@echo "Running "$c" on $(arg1) RDS"
	cd enviroments/$(arg1)/data-storage/postgreSQL/; terragrunt $c
