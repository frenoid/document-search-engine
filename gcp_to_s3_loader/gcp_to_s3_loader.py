import os
import io
import json
import boto3
import glob
import pandas as pd

from __future__ import annotations
from typing import NewType
from os.path import join, exists, splitext, basename
from datetime import datetime, timedelta
from boto3_type_annotations.s3 import Client
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload    

from google.auth.exceptions import MutualTLSChannelError
from googleapiclient.errors import HttpError
from botocore.exceptions import NoCredentialsError, ClientError


GCPClient = NewType('GCPClient', Resource)
S3Client = NewType('S3Client', Client)

def read_json(file_path): 
    with open(file_path, "r") as f:
        return json.load(f)
def run(config: dict) -> None:

    # create necessary service folder structure 
    for folder, folder_path in config['SERVICE']['FILE']:
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    # establish connections to GCP and S3
    gcp_client = get_gcp_client(config)
    s3_client = get_s3_client(config)

    # fetch new files list from gcp
    time_interval = config['GCP']["GCP_QUERY_INTERVAL"]
    newFiles = get_new_files(gcp_client, time_interval)

    # download new files if there's any and stage all new files
    status = False
    if not newFiles:
        status = download_in_bulk(gcp_client, newFiles, config)
        staging_files(config)
    
    # upload staged files
    if status:
        upload_to_bucket(s3_client, config)

def get_gcp_client(config: dict) -> GCPClient:
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    credential_path = config['GCP']['GCP_CREDENTIAL']
    token_path = config['GCP']['GCP_TOKEN']
    scope = config['GCP']['GCP_SCOPE']
    port = config['GCP']['GCP_CONNECT_PORT']
    creds = None
    
    try: 
        if exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scope)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_path, scope
                )
                creds = flow.run_local_server(port=port)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        service = build('drive', 'v3', credentials=creds)
        return service
    except MutualTLSChannelError as e:
        print(f"Error! Error connecting to GCP client: {e}") 


def get_s3_client(config: dict) -> S3Client:
    access_key = config['S3']['S3_ACCESS_KEY']
    secret_key = config['S3']['S3_SECRET_KEY']
    try:
        s3 = boto3.client(
            's3', 
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key
        )
    except NoCredentialsError:
        print("Error! Invalid Credential to s3")
    except ClientError as e:
        if e.response['Error']['Code'] == 'Internal Error':
            http_status_code = e.response['ResponseMetadata']['HTTPStatusCode']
            error_message = e.response['Error']['Message']
            print(f'Error! Error connecting to S3 client. Error code {http_status_code}: {error_message}')

def get_new_files(gcp_client: GCPClient, interval: int) -> list[dict]:
    # Taking the resource obj and return a list of the new files for the past 24 hours
    new_files = []
    try: 
        results = gcp_client.files().list(
            pageSize=10, 
            fields="nextPageToken, files(id, name, mimeType, createdTime)"
        ).execute()
        items = results.get('files', [])
        
        if not items:
            print('No files found.')
        else: 
            benchmark = datetime.now() - timedelta(hours = interval)
            for item in items:
                if datetime.strptime(item['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ') > benchmark:
                    new_files.append(item.copy())
    except HttpError as error:
        print(f'Error! An http error occured during querying new files: {error}')
    return new_files


def download(gcp_client: GCPClient, file: dict, base_dir: str) -> bool:
    # Taking the resource obj and individual file info (filename, id, file type) to download to the base dir
    try:  
        filename = file['name']
        request = gcp_client.files().get_media(fileId=file['id'])
        fh = io.FileIO(join(base_dir, f'{filename}'), mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(status)
            if status:
                print("Download %d%%. " % int(status.progress()*100))
        print(f"Success! Download {filename} Complete!")
        return True
    except HttpError as error:
        print(f'Error! An Http error occurred: {error}')
        return False
    except KeyError:
        print(f'Error! Incorrect or empty file input')
        return False


def download_in_bulk(gcp_client: GCPClient, files: list[dict], config: dict) -> None:
    new_file_dir = config['SERVICE']['FILE_PATH']['NEW_FILES_DIR']
    # Taking the resource obj and list of files to download each of them to the base dir
    if files:
        for file in files:
            download(gcp_client, file, new_file_dir)
    else:
        print('No new files created for the past day')

def staging_files(config: dict) -> None:
    new_files_dir = config['SERVICE']['FILE_PATH']['NEW_FILES_DIR']
    staged_files_dir = config['SERVICE']['FILE_PATH']['STAGED_FILES_DIR']
    # Staging new CSV files, split individual files into small files of 10 rows each, save them into STAGED_FILES_DIR
    files = glob.glob(join(new_files_dir,'*.csv'))
    if not files:
        print("No new files uploaded for the past 24 hours")
    else:
        for file_path in files:
            fileName = basename(file_path)
            try:
                data = pd.read_csv(file_path)
                for i in range(data.shape[0]//10):
                    next_chunk = join(staged_files_dir, f'{splitext(fileName)[0]}_{i}.csv')
                    data.iloc[i*10:(i+1)*10,:].to_csv(next_chunk)
                print(f'Success! Successfully process file: {fileName}')
                os.remove(file_path)
            except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                print(f"Error! Error to read {fileName}: {e}")

def upload_to_bucket(s3_client: S3Client, config: dict) -> None:
    # Upload all files in STAGED_FILES_DIR to S3 bucket, move files into RELEASED_FILES_DIR after successful upload
    staged_files_dir = config['SERVICE']['FILE_PATH']['STAGED_FILES_DIR']
    released_files_dir = config['SERVICE']['FILE_PATH']['RELEASED_FILES_DIR']
    error_files_dir = config['SERVICE']['FILE_PATH']['ERROR_FILES_DIR']
    bucket = config['S3']['S3_BUCKET_NAME']

    for root, dirs, files in os.walk(staged_files_dir):
        for file in files:
            new_file = join(root, file)
            released_file = join(released_files_dir, file)
            error_file = join(error_files_dir, file)
            try:
                s3_client.upload_file(new_file, bucket, file)
                os.replace(new_file, released_file)
                print(f"Success! Upload {file} to {bucket} Successful")
            except ClientError:
                print(f'Error! Client error uploading file {file}, move file to the error file folder')
                os.replace(new_file, error_file)
            except NoCredentialsError:
                print('Error! Credentials not available')

if __name__ == '__main__':
    config = read_json("config.json")
    run(config)
