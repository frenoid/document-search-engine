# ------------------------------------------------------------------------------
# CREATE EC2 Instances
# ------------------------------------------------------------------------------
resource "aws_instance" "gcp-to-s3-loader-service" {
    ami = "ami-0fab0953c3bb514a9"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["<security_group_here"]

    tags = {
        Name = "gcp-to-s3-loader-service"
    }
  
}

resource "aws_instance" "doc-search-backend" {
    ami = "ami-05b10160400f5d51e"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["<security_group_here"]

    tags = {
        Name = "doc-search-backend"
    }
  
}

resource "aws_instance" "document-db" {
    ami = "ami-0d97c93b6ac5342f6"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["<security_group_here"]

    tags = {
        Name = "document-db"
    }
  
}

resource "aws_instance" "djangoapp" {
    ami = "ami-03ca998611da0fe12"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["<security_group_here"]

    tags = {
        Name = "djangoapp"
    }
  
}

resource "aws_instance" "es-loader-service" {
    ami = "ami-0fab0953c3bb514a9"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["<security_group_here"]

    tags = {
        Name = "es-loader-service"
    }
  
}

# ------------------------------------------------------------------------------
# CREATE AWS Security Group
# ------------------------------------------------------------------------------
resource "aws_security_group" "allow_all" {
    name = "allow_all"

    ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "allow_all_connection"
    }
}