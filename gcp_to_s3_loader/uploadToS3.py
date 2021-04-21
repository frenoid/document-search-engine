import boto3
from botocore.exceptions import NoCredentialsError
import os

ACCESS_KEY = ''
SECREDT_KEY = ''


FILE_DIR = "./files"

def upload_to_aws(path, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECREDT_KEY)

    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                s3.upload_file(os.path.join(root, file), bucket, file)
                print("Upload {} to {} Successful".format(file, bucket))
            return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

