import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = "./credentials.json"
TOKEN_FILE = 'token.json'
FOLDER_ID = '1PdkMTPyTxqkhdUgjAmZwhvDPFxc5ZdmW'
FOLDER_PATH = "./folder"  # Folder from which to upload files

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_file(credentials, file_path, folder_id):
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded {os.path.basename(file_path)} with file ID: {file.get('id')}")

def upload_folder_contents(credentials, folder_path, folder_id):
    for item in os.listdir(folder_path):
        file_path = os.path.join(folder_path, item)
        if os.path.isfile(file_path):
            upload_file(credentials, file_path, folder_id)

if __name__ == '__main__':
    creds = authenticate()
    upload_folder_contents(creds, FOLDER_PATH, FOLDER_ID)
