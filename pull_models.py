# pull_models.py

#Manual use:
#MODEL_FILE_ID="1a2b3c4d5e6f"
#python3 pull_models.py


import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials
from cassandra.cluster import Cluster
import io

# 1. Modell-File-ID aus Umgebungsvariable laden
model_file_id = os.getenv('MODEL_FILE_ID')
if not model_file_id:
    raise ValueError("MODEL_FILE_ID environment variable not set")

# 2. Google Drive API Setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_FILE = 'credentials.json'

def download_model_from_drive(file_id, destination):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Download progress: {int(status.progress() * 100)}%')
    
    print(f'Model downloaded to {destination}')

# 3. Modell von Google Drive herunterladen
destination = '/tmp/model.h5'
download_model_from_drive(model_file_id, destination)

# 4. Cassandra Setup
cluster = Cluster(['your_cassandra_host'])
session = cluster.connect('your_keyspace')

# 5. Modell in Cassandra laden
def save_model_to_cassandra(model_path):
    with open(model_path, 'rb') as f:
        model_data = f.read()

    query = "INSERT INTO models (model_id, model_data) VALUES (%s, %s)"
    session.execute(query, ('model_1', model_data))

save_model_to_cassandra(destination)
print("Model saved to Cassandra")

# 6. Cleanup (optional)
os.remove(destination)
