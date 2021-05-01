## DocumentDB to ES Loader

Functions to download newly created files from Google Drive, divide files into smaller files with 10 records each, and upload them onto desired folder under the target S3 bucket

#### Setup

```
$ mkvirtualenv -p python3 gcp_to_s3_loader
$ pip3 install -r requirements.txt
```
#### Configuration

Create a `config.json` file with the following contents. A `config_sample.json` file is provided as an example. 

```
{
    "SERVICE": {
        "FILE": {
            "NEW_FILES_DIR": "./new_files",
            "STAGED_FILES_DIR": "./staged_files",
            "RELEASED_FILES_DIR": "./released_files",
            "ERROR_FILES_DIR": "./error_files"
        }
    },
    "GCP": {
        "GCP_CREDENTIAL": "<GCP Credential JSON>",
        "GCP_TOKEN": "<GCP Token JSON>",
        "GCP_SCOPE": ["https://www.googleapis.com/auth/drive.readonly"],
        "GCP_CONNECT_PORT": 8080,
        "GCP_QUERY_INTERVAL": 24
    },
    "S3": {
        "S3_ACCESS_KEY": "<AWS ACCESS KEY>",
        "S3_SECRET_KEY": "<AWS SECRET KEY>",
        "S3_BUCKET_NAME": "<S3 BUCKET NAME>",
        "S3_UPLOAD_FOLDER_NAME": "<FOLDER NAME>"
    }
}
```