# SWE 5001 Architecting Scalable Systems - Practice Module Project

![Tests](https://github.com/github/docs/actions/workflows/tests.yml/badge.svg)

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

TBC
