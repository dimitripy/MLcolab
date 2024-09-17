import os
import json
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Standardkonfigurationsargumente für den DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG initialisieren
dag = DAG(
    'PingPong_DAG_Test',
    default_args=default_args,
    description='Ein einfacher Ping Pong DAG',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['test'],
)

# Konfigurationsdateipfad
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.json')

# Lade Konfigurationsdatei
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

# Hol die ngrok-URL aus der Konfigurationsdatei
ngrok_url = config.get('ngrok_url')

# Funktion zum Senden von "Ping" und Verarbeitung der Antwort "Pong"
def send_ping():
    payload = {'message': 'Ping'}
    print(f"Sende Ping an den Coworker über URL: {ngrok_url}...")
    
    response = requests.post(ngrok_url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Antwort vom Coworker: {result}")
        if result.get('reply') == 'Pong':
            print("Pong empfangen, Aufgabe erfolgreich abgeschlossen.")
        else:
            raise ValueError(f"Unerwartete Antwort: {result.get('reply', 'keine Antwort')}")
    else:
        raise ConnectionError(f"Fehler bei der Verbindung zum Coworker. Status Code: {response.status_code}")

# Funktion zum Senden von "Ding" und Verarbeitung der Antwort "Dong"
def send_ding():
    payload = {'message': 'Ding'}
    print(f"Sende Ding an den Coworker über URL: {ngrok_url}...")
    
    response = requests.post(ngrok_url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Antwort vom Coworker: {result}")
        if result.get('reply') == 'Dong':
            print("Dong empfangen, Aufgabe erfolgreich abgeschlossen.")
        else:
            raise ValueError(f"Unerwartete Antwort: {result.get('reply', 'keine Antwort')}")
    else:
        raise ConnectionError(f"Fehler bei der Verbindung zum Coworker. Status Code: {response.status_code}")

# Aufgaben im DAG definieren
task_ping = PythonOperator(
    task_id='send_ping',
    python_callable=send_ping,
    dag=dag,
)

task_ding = PythonOperator(
    task_id='send_ding',
    python_callable=send_ding,
    dag=dag,
)

# Reihenfolge der Aufgaben definieren
task_ping >> task_ding
