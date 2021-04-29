# AWS lambda MongoDB loader

## Overview
This event-driven lambda function watches the *nus-iss-group-3* S3 bucket for new csv files, reads them then uploads the content into *MongoDB*.

### Source
S3 files in csv format
See ./example.csv for the expected format

### Sink
MongoDB 

### Trigger
Lambda function mongo-loader-function triggers when an object is created in *s3://nus-iss-group-3* via PUT or POST

### Actions
The lambda function reads the csv file row-by-row and inserts the document into the MongoDB

### To deploy
Zip all python dependencies into *my-deployment-package.zip*

E.g.
```
mongodb-loader-function
 |
 ---lambda_function.py
 ---/packageA
 ---/packageB
 ---/packageC
```


Run the following in the CLI
```aws lambda update-function-code --function-name mongo-loader-function --zip-file fileb://my-deployment-package.zip```