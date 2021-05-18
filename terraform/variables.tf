variable "aws_region" {
    description = "Region we use for deploying all AWS instances"
    type = string
    default = "ap-southeast-1"
}
variable "aws_access_key" {
    type = string
    default = "<Input your access key here>"
}
variable "aws_secret_key" {
    type = string
    default = "<Input your secret key here>"
}
variable "ec2_key_name" {
    type = string
    default = "nus-iss-group3"
} 
variable "lambda_arn_role" {
    type = string
    default = "MongoDBLoader"
}

variable "default_ec2_ami" {
    type = string
    default = "ami-0fab0953c3bb514a9"
}

variable "default_ec2_instance_type" {
    type = string
    default = "t2.micro"
}