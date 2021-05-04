## Terraform to setup the infrastructure

Terraform code to document the infrastructure we need for running all the service.

#### Setup

Make sure you have terraform installed on your drive.
You can download Terraform here: https://www.terraform.io/downloads.html

```
$ terraform init
$ terraform plan 
$ terraform apply
```
#### Configuration

You can configure the aws access key and secret under `variables.tf` file with the following contents. 

```
variable "aws_access_key" {
    type = string
    default = "<Input your access key here>"
}
variable "aws_secret_key" {
    type = string
    default = "<Input your secret key here>"
}
```