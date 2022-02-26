# get a aws bastion instance to communicate private subnet.

# retrive aws ami information 
data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-kernel-5.10-hvm-2.0.*-x86_64-gp2"]
  }
  owners = ["amazon"]
}

# create aws ec2 instance from data 
resource "aws_instance" "bastion" {

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"

  user_data = file("./templates/bastion/user-data.sh")

  tags = merge(
    local.common_tags,
    tomap({ Name = "${local.prefix}-bastion" })
  )


}
