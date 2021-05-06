# SWE 5001 Architecting Scalable Systems - Practice Module Project

![Tests](https://github.com/frenoid/document-search-engine/actions/workflows/tests.yml/badge.svg)
![Build](https://github.com/frenoid/document-search-engine/actions/workflows/build.yml/badge.svg)

## A search engine for company documentation

The company has many teams writing technical documentation on Google Docs for their products and processes.

But knowledge sharing across teams is hard because there is no good way to search the body of text on Google Docs.

In addition, employees find some documents especially useful and want to highlight them in search results.

We propose building a search engine for the company’s documentation that learns which documents are useful to employees and helps employees find them.

For more info, see https://docs.google.com/document/d/1iPhPTKiz3b44uG7y99aJp4WtUJptwGFWjQ8SRrf9LaE/edit

## Architecture

![Architecture diagram](https://github.com/frenoid/document-search-engine/blob/master/architecture.png?raw=true)

## Our Platform

### Seed
Need for documentation readers to find documents relevant to them. In return documentation writers find their intended audience and get feedback on how to write better documentation

### Magnet
For the publishers: modular integration with multiple document sources. Wherever you write,  you can integrate with our system (GDocs, GDrive, OnDrive, Dropbox).
For the publishers: get the documentation seen by the right people if they connect to our system.
For the consumers: always find the documentation you really want.
For the consumers: search engine improves results the more you use it.
For the consumers: search results are continuously improved with the internally developed feedback loop to collect and learn from users’ search history and feedback.

### Producers
Documentation writers


### Consumers
Documentation readers
We propose a platform to enable the following use cases
Teams can publish documentation to a Cloud Storage
The platform can index the text in the Cloud Storage
The platform can make these documents easily searchable
Teams needing the documentation can easily find the documents they want on the platform
Document consumers can give feedback on the documentation and rank the documentation by usefulness
The platform will improve the search algorithm to give better results based on user feedback
The platform will record user views and behaviour on the platform and use machine learning to recommend other useful documents to each user


## To Run

### Setup all cloud resources with Terraform configuration
All the cloud infrastructure included in this project are documented as Terraform configuration. This helps to improve the maintanabiltiy and extensibiltiy. Teams are allow to build, change and version the infrastructure safely and efficiently. It also makes redeployment in different environments simpler. Users are able to scale up/down the resource via configuration update and re-apply. It's also a easier way for management to have an overview on all the resources plan, monitoring the usage and make necessary adjustment at ease. 

Terraform structure
```
.
└── terraform
    ├── versions.tf
    ├── variables.tf
    ├── provider.tf
    ├── main.tf
    ├── env_init.sh
```
How to run:
```
cd terraform
terraform init
terraform plan
terraform apply
```

Files included:
* versions.tf: document the terraform and required service provider versions.
* variables.tf: document the necessary environment variales (e.g. key-names, iam role)
* provider.tf: document the necessary provider configuration
* main.tf: document all resources' configuration, set up based on service nature
* env_init.sh: script to execute when creating the defined EC2 instance, to ensure instances are created with necessary package installed and environment variables enabled
