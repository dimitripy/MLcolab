import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import git

def setup_colabside(project_name, repo_url, branch, ngrok_authtoken, port):
    # Authentifizierung bei Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentifizierung im lokalen Webbrowser
    drive = GoogleDrive(gauth)

    # Erstellen eines Verzeichnisses auf Google Drive
    folder_metadata = {
        'title': project_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    folder_id = folder['id']
    print(f'Projektverzeichnis erstellt mit ID: {folder_id}')

    # Lokales Verzeichnis für das Git-Projekt
    local_project_path = os.path.join(os.getcwd(), project_name)

    # Git-Projekt klonen
    if not os.path.exists(local_project_path):
        os.makedirs(local_project_path)
    git.Repo.clone_from(repo_url, local_project_path, branch=branch)
    print(f'Git-Projekt geklont nach: {local_project_path}')

    # Konfigurationsdaten
    config_data = {
        'ngrok_authtoken': ngrok_authtoken,
        'port': port
    }

    # Konfigurationsdatei erstellen
    config_path = os.path.join(local_project_path, 'config.json')
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print(f'Konfigurationsdatei erstellt in: {config_path}')

    # .env Datei erstellen
    env_content = f"""NGROK_AUTHTOKEN={ngrok_authtoken}
    PROJECT_PATH_TEMPLATE={local_project_path}
    PORT={port}
    """
    create_env_file(local_project_path, env_content)

def create_env_file(target_dir, env_content):
    env_file_path = os.path.join(target_dir, '.env')
    with open(env_file_path, 'w') as env_file:
        env_file.write(env_content)
    print(f".env Datei wurde erfolgreich erstellt unter: {env_file_path}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 6:
        print("Usage: python import_colabside.py <project_name> <repo_url> <branch> <ngrok_authtoken> <port>")
        sys.exit(1)
    setup_colabside(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])