# Temporary File 

1). create AWS CLI user. Assign user with MFA and Admin access policy.
2). Use aws-vault package. https://github.com/99designs/aws-vault
3). Use terraform in docker to lock version. The AWS_ACESS_KEY, AWS_SECRET_KEY and AWS_SECTION_TOKEN are set from aws-vault and access in dockerfile.
4). Use terraform workspace to create ,dev, staging, prod evnironment.
5). Setup ssh access to bastion.
6). Create terraform.tfvars to store db_user and db_password, which is copied from sample.tfvars.
