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



resource "aws_iam_role" "bastion" {
  name               = "${local.prefix}-bastion"
  assume_role_policy = file("./templates/bastion/instance-profile-policy.json")

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "bastion_attach_policy" {
  role       = aws_iam_role.bastion.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "bastion" {
  name = "${local.prefix}-bastion-instance-profile"
  role = aws_iam_role.bastion.name
}



# create aws ec2 instance from data 
resource "aws_instance" "bastion" {

  ami = data.aws_ami.amazon_linux.id

  instance_type = "t2.micro"



  user_data = file("./templates/bastion/user-data.sh")
  # iam role 
  iam_instance_profile = aws_iam_instance_profile.bastion.name
  # assign to public subnet
  subnet_id = aws_subnet.public_a.id
  # add ssh key to acess
  key_name = var.bastion_key_name

  # assign security group
  vpc_security_group_ids = [
    aws_security_group.bastion.id
  ]


  tags = merge(
    local.common_tags,
    tomap({ Name = "${local.prefix}-bastion" })
  )


}



# allow limit inbound and outbound

resource "aws_security_group" "bastion" {
  description = "Control bastion inbound and outbound access"
  name        = "${local.prefix}-bastion"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol = "tcp"
    # https
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol = "tcp"
    # http
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    # postgres
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private_a.cidr_block,
      aws_subnet.private_b.cidr_block,
    ]
  }

  tags = local.common_tags
}
