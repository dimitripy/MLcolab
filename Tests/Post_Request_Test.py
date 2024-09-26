import requests
import json
import os

# Verzeichnis des aktuellen Skripts ermitteln
script_dir = os.path.dirname(os.path.abspath(__file__))

# Pfad zur Konfigurationsdatei relativ zum Skriptverzeichnis setzen
config_path = os.path.join(script_dir, 'config.json')

# Laden der Konfiguration aus der Datei
with open(config_path, 'r') as f:
    config = json.load(f)

# ngrok URL aus der Konfigurationsdatei lesen
ngrok_url = config.get('ngrok_url')

if not ngrok_url:
    raise ValueError('ngrok_url ist nicht in der Konfigurationsdatei gesetzt.')

# Vollständige URL für die /health Route
health_url = f'{ngrok_url}/health'

# GET-Anfrage an die /health Route senden
response = requests.get(health_url)

# Antwort ausdrucken
print('Status Code:', response.status_code)
print('Response Text:', response.text)