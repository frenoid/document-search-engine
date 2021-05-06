# ------------------------------------------------------------------------------
# CREATE EC2 Instances
# ------------------------------------------------------------------------------
# GCP to S3 Loader service
resource "aws_instance" "gcp-to-s3-loader-service" {
    ami = "ami-0fab0953c3bb514a9"
    instance_type = "t2.micro"
    key_name = var.ec2_key_name
    security_groups = ["<security_group_here"]

    tags = {
        Name = "gcp-to-s3-loader-service"
    }
  
}
# Elastic Search loader service
resource "aws_instance" "es-loader-service" {
    ami = "ami-0fab0953c3bb514a9"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["<security_group_here"]

    tags = {
        Name = "es-loader-service"
    }

}
# Document DB
resource "aws_instance" "document-db" {
    ami = "ami-0d97c93b6ac5342f6"
    instance_type = "t2.micro"
    key_name = var.ec2_key_name
    security_groups = ["<security_group_here"]

    tags = {
        Name = "document-db"
    }
  
}
# Document Search Backend Service
resource "aws_instance" "doc-search-backend" {
    ami = "ami-05b10160400f5d51e"
    instance_type = "t2.micro"
    key_name = var.ec2_key_name
    security_groups = ["<security_group_here"]

    tags = {
        Name = "doc-search-backend"
    }
  
}
# Django app server
resource "aws_instance" "djangoapp" {
    ami = "ami-03ca998611da0fe12"
    instance_type = "t2.micro"
    key_name = var.ec2_key_name
    security_groups = ["<security_group_here"]

    tags = {
        Name = "djangoapp"
    }

}
# ------------------------------------------------------------------------------
# CREATE Elastic Search Domain
# ------------------------------------------------------------------------------
resource "aws_elasticsearch_domain" "doc-search" {
    domain_name = "doc-search"
    elasticsearch_version = "7.9"

    cluster_config {
        instance_type = "t3.small.elasticsearch"
        instance_count = 1
    }

    ebs_options {
       ebs_enabled = true
       volume_size = 10
    }

    tags = {
        Domain = "doc-search"
    }

}

# ------------------------------------------------------------------------------
# CREATE S3 Instance
# ------------------------------------------------------------------------------
resource "aws_s3_bucket" "build-artifacts" {
    bucket = "build-artifacts-bucket" 
    acl = "private"

    tags = {
        name = "group3-build-artifacts"
        Environment = "Dev"
    }
} 

# ------------------------------------------------------------------------------
# CREATE Lambda Functions
# ------------------------------------------------------------------------------
resource "aws_lambda_function" "mongo-loader-function" {
    function_name = "mongo-loader-function"
    role = var.lambda_arn_role
    rntime = "python3.8"
    memory_size = 512
    timeout = 30
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