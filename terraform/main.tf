# ------------------------------------------------------------------------------
# CREATE EC2 Instances
# ------------------------------------------------------------------------------
# GCP to S3 Loader service
resource "aws_instance" "gcp-to-s3-loader-service" {
    ami = var.default_ec2_ami
    instance_type = var.default_ec2_instance_type
    key_name = var.ec2_key_name
    security_groups = ["documentdb"]

    tags = {
        Name = "gcp-to-s3-loader-service"
        ASG = "ASG-EC2-1"
    }
  
    provisioner "local-exec" {
        command = "/bin/bash env_init.sh"
    }
}
# Elastic Search loader service
resource "aws_instance" "es-loader-service" {
    ami = var.default_ec2_ami
    instance_type = var.default_ec2_instance_type
    key_name = var.ec2_key_name
    security_groups = ["documentdb"]

    tags = {
        Name = "es-loader-service"
        ASG = "ASG-EC2-1"
    }

    provisioner "local-exec" {
        command = "/bin/bash env_init.sh"
    }
}
# Document DB
resource "aws_instance" "document-db" {
    ami = var.default_ec2_ami
    instance_type = var.default_ec2_instance_type
    key_name = var.ec2_key_name
    security_groups = ["documentdb"]

    tags = {
        Name = "document-db"
        ASG = "ASG-EC2-1"
    }
  
    provisioner "local-exec" {
        command = "/bin/bash env_init.sh"
    }

}
# Document Search Backend Service
resource "aws_instance" "doc-search-backend" {
    ami = var.default_ec2_ami
    instance_type = var.default_ec2_instance_type
    key_name = var.ec2_key_name
    security_groups = ["documentdb"]

    tags = {
        Name = "doc-search-backend"
        ASG = "ASG-EC2-1"
    }

    provisioner "local-exec" {
        command = "/bin/bash env_init.sh"
    }

}
# Django app server
resource "aws_instance" "djangoapp" {
    ami = var.default_ec2_ami
    instance_type = var.default_ec2_instance_type
    key_name = var.ec2_key_name
    security_groups = ["documentdb"]

    tags = {
        Name = "djangoapp"
        ASG = "ASG-EC2-1"
    }
    
    provisioner "local-exec" {
        command = "/bin/bash env_init.sh"
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
# CREATE AWS Security Rule
# ------------------------------------------------------------------------------
resource "aws_security_group" "documentdb" {
    name = "allow_all"

    ingress = [ 
        {
            description = "SSH"
            from_port = 22
            to_port = 22
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        },
        {
            description = "custom TCP rule"
            from_port = 27017
            to_port = 27019
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        } 
    ]

    egress {
        description = "Egress rule for retrieve and refresh GCP token"
        from_port   = 8000
        to_port     = 8000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "ssh and mongodb"
    }
}
# ------------------------------------------------------------------------------
# CREATE AWS EC2 Auto-scaling group
# ------------------------------------------------------------------------------

resource "aws_launch_configuration" "asg-ec2-1-provisioner" {
    name_prefix   = "asg-ec2-1-provisioner-"
    image_id      = var.default_ec2_ami
    instance_type = var.default_ec2_instance_type

    lifecycle {
        create_before_destroy = true
    }
}

resource "aws_autoscaling_group" "asg-ec2-1" {
    name     = "asg-ec2-1"
    max_size = 5
    min_size = 1

    launch_configuration = "${aws_launch_configuration.asg-ec2-1-provisioner.name}"
    health_check_type    = "EC2"
    default_cooldown     = 60
}

resource "null_resource" "provision_task" {
    triggers {
        lc_name = "${aws_autoscaling_group.asg-ec2-1.launch_configuration}"
    }

    provisioner "local-exec" {
        command = "/bin/bash env_init.sh"
    }
}