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