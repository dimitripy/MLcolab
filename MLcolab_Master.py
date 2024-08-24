import json
import papermill as pm
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials
import io
import os
from cassandra.cluster import Cluster

# 1. Konfigurationsdatei erstellen/aktualisieren
config = {
    "data_url": "https://yourserver.com/data.csv",  # TODO
    "features": ["SMA_50", "SMA_200", "RSI", "MACD", "MACD_signal"],
    "labels": "trend",
    "model_output_path": "path/to/save/model.h5",
    "parameters": {
        "epochs": 10,
        "batch_size": 32
    },
    "ssh_config": {  # SSH-Parameter werden in die JSON aufgenommen
        "trigger_pull_script": True,  # Kontrolle, ob der SSH-Trigger aktiviert ist
        "server": "your_server_ip",
        "user": "your_username",
        "key_file": "/path/to/your/private_key.pem",
        "script_path": "/path/to/pull_models.py"
    }
}

config_path = 'config.json'
with open(config_path, 'w') as config_file:
    json.dump(config, config_file)

# 2. Daten vorbereiten (falls erforderlich)
# TODO: Datenvorbereitungscode hier einfügen

# 3. Ausführen des Notebooks mit Papermill
notebook_input_path = 'MLcolab_Worker.ipynb'
notebook_output_path = 'MLcolab_Worker_output.ipynb'

pm.execute_notebook(
    notebook_input_path,
    notebook_output_path,
    parameters=config
)

# Optional: Modell herunterladen und in Cassandra speichern
def download_model_from_drive(file_id, destination):
    scopes = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account_credentials.json', scopes)
    drive_service = build('drive', 'v3', credentials=creds)

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Download progress: {int(status.progress() * 100)}%')

def save_model_to_cassandra(model_path):
    cluster = Cluster(['your_cassandra_host'])
    session = cluster.connect('your_keyspace')
    
    with open(model_path, 'rb') as f:
        model_data = f.read()
    
    query = "INSERT INTO models (model_id, model_data) VALUES (%s, %s)"
    session.execute(query, ('model_1', model_data))
    print("Model saved to Cassandra")

# Überprüfen, ob das Modell heruntergeladen und in Cassandra gespeichert werden soll
if config['ssh_config']['trigger_pull_script'] is False:
    model_file_id = 'YOUR_MODEL_FILE_ID'  # TODO: Aktualisieren Sie die File ID
    model_local_path = 'model.h5'
    download_model_from_drive(model_file_id, model_local_path)
    save_model_to_cassandra(model_local_path)
