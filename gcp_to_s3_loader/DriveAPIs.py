from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
import json
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def connect(credential_file):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_file, SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def get_new_files(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, mimeType, createdTime)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        res = []
        last24HourDateTime = datetime.now() - timedelta(hours = 24)
        for item in items:
            if datetime.strptime(item['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ') > last24HourDateTime:
                res.append(item.copy())
        return res


def download(service, file_name, file_id, file_mimeType):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO('{}'.format(file_name), mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(status)
        if status:
            print("Download %d%%. " % int(status.progress()*100))
    print("Download Complete!")

def download_new_files(service, new_files):
    if new_files:
        for new_file in new_files:
            download(service, new_file['name'], new_file['id'], new_file['mimeType'])
    else:
        print('No new files created for the past day')

if __name__ == '__main__':
    service = connect('credential_test.json')
    new_files = get_new_files(service)
    download_new_files(service, new_files)
