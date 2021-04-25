import boto3
from botocore.exceptions import NoCredentialsError
import os
from os.path import splitext, basename
import glob
import pandas as pd
    

def staging_files():
    # Staging new CSV files, split individual files into small files of 10 rows each, save them into STAGED_FILES_DIR
    files = glob.glob(os.path.join(os.environ.get('NEW_FILES_DIR'),'*.{}'.format('csv')))
    if files:
        try:
            for file_path in files:
                fileName = basename(file_path)
                data = pd.read_csv(file_path)
                for i in range(data.shape[0]//10):
                    data.iloc[i*10:(i+1)*10,:].to_csv(os.path.join(os.environ.get('STAGED_FILES_DIR'), '{}_{}.csv').format(splitext(fileName)[0], i))
                print('Successfully process file: {}'.format(fileName))
                os.remove(file_path)
        except Exception as e:
            os.replace(file_path, os.path.join(os.environ.get("FAILED_FILES_DIR"),'{}.csv'.format(fileName)))
            print("Error {} processing file: {}".format(e, fileName))
    else:
        print("No new files uploaded for the past 24 hours")

def upload_to_aws(bucket):
    # Upload all files in STAGED_FILES_DIR to S3 bucket, move files into RELEASED_FILES_DIR after successful upload
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'),aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
    try:
        for root, dirs, files in os.walk(os.environ.get('STAGED_FILES_DIR')):
            for file in files:
                s3.upload_file(os.path.join(root, file), bucket, file)
                os.replace(os.path.join(root, file), os.path.join(os.environ.get('RELEASED_FILES_DIR', file)))
                print("Upload {} to {} Successful".format(file, bucket))
            return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

if __name__ == '__main__':
    staging_files()
    upload_to_aws(os.environ.get('S3_BUCKET'))