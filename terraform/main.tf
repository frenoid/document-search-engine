resource "aws_instance" "test_ec2" {
    ami = "ami-0fab0953c3bb514a9"
    instance_type = "t2.micro"
    key_name = "nus-iss-group3"
    security_groups = ["documentdb"]

    tags = {
        Name = "myFirstTest"
    }
  
}