from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import requests
import os
import json
from datetime import timedelta

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
    'PingPong_light_Test',
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

# Hol die ngrok_url aus der Konfigurationsdatei
ngrok_url = config.get('ngrok_url')

def trigger_coworker_script_ping():
    payload = {
        'project': 'MLcoworker',
        'branch': 'slim',
        'script': 'ping_pong.py',
        'parameters': ['ping']  # Übergabeparameter hier
    }
    print(f"Sende Ping an den Coworker über ngrok_url: {ngrok_url}...")
    
    response = requests.post(ngrok_url, json=payload)
    if response.status_code == 200:
        print("Erfolg: ", response.text)
    else:
        print("Fehler: ", response.text)

def trigger_coworker_script_ding():
    payload = {
        'project': 'MLcoworker',
        'branch': 'slim',
        'script': 'ding_dong.py',
        'parameters': ['ding']  # Übergabeparameter hier
    }
    response = requests.post(ngrok_url, json=payload)
    if response.status_code == 200:
        print("Erfolg: ", response.text)
    else:
        print("Fehler: ", response.text)
        
task_ping = PythonOperator(
    task_id='send_ping',
    python_callable=trigger_coworker_script_ping,
    dag=dag,
)

task_ding = PythonOperator(
    task_id='send_ding',
    python_callable=trigger_coworker_script_ding,
    dag=dag,
)

# Reihenfolge der Aufgaben definieren
task_ping >> task_ding

