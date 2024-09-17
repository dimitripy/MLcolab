import requests

# Laden der Konfiguration aus der Datei
with open('config.json', 'r') as f:
    config = json.load(f)

ngrok_url = config.get('ngrok_url')

if not ngrok_url:
    raise ValueError('ngrok_url ist nicht in der Konfigurationsdatei gesetzt.')

# Daten, die in der POST-Anfrage gesendet werden sollen
data = {
    'step': 'example_step'
}

# POST-Anfrage senden
response = requests.post(ngrok_url, json=data)

# Antwort ausdrucken
print('Status Code:', response.status_code)
print('Response Text:', response.text)
