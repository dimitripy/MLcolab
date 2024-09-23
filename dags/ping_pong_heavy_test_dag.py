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
    'PingPong_Heavy_Test',
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

def trigger_coworker_script_test(test_case):
    payload = {
        'project': 'pingpong-test',
        'branch': 'main',
        'script': 'ping_pong.py',
        'parameters': ['ping']
    }

    expected_status_code = 200
    expected_message = "pong"

    if test_case == 1:
        payload['project'] = 'wrong_project'
        expected_status_code = 400
        expected_message = "Fehler: Ungültiges Projekt"
    elif test_case == 2:
        payload['branch'] = 'wrong_branch'
        expected_status_code = 400
        expected_message = "Fehler: Ungültiger Branch"
    elif test_case == 3:
        payload['script'] = 'non_existent_script.py'
        expected_status_code = 400
        expected_message = "Fehler: Skript nicht gefunden"
    elif test_case == 4:
        payload['parameters'] = ['wrong_parameter']
        expected_status_code = 400
        expected_message = "Ungültiger Parameter: wrong_parameter"
    elif test_case == 5:
        expected_message = "dong"
        payload['script'] = 'ding_dong.py'
        payload['parameters'] = ['ding']
    elif test_case == 6:
        expected_message = "pong"

    print(f"Sende Testfall {test_case} an den Coworker über ngrok_url: {ngrok_url}...")
    
    response = requests.post(ngrok_url, json=payload)
    if response.status_code == expected_status_code and expected_message in response.text:
        print(f"Testfall {test_case} erfolgreich: {response.text}")
    else:
        raise ValueError(f"Testfall {test_case} fehlgeschlagen: {response.text}")

task_test_1 = PythonOperator(
    task_id='test_wrong_project',
    python_callable=lambda: trigger_coworker_script_test(1),
    dag=dag,
)

task_test_2 = PythonOperator(
    task_id='test_wrong_branch',
    python_callable=lambda: trigger_coworker_script_test(2),
    dag=dag,
)

task_test_3 = PythonOperator(
    task_id='test_non_existent_script',
    python_callable=lambda: trigger_coworker_script_test(3),
    dag=dag,
)

task_test_4 = PythonOperator(
    task_id='test_wrong_parameter',
    python_callable=lambda: trigger_coworker_script_test(4),
    dag=dag,
)

task_test_5 = PythonOperator(
    task_id='test_successful_ding',
    python_callable=lambda: trigger_coworker_script_test(5),
    dag=dag,
)

task_test_6 = PythonOperator(
    task_id='test_successful_ping',
    python_callable=lambda: trigger_coworker_script_test(6),
    dag=dag,
)

# Reihenfolge der Aufgaben definieren
task_test_1 >> task_test_2 >> task_test_3 >> task_test_4 >> task_test_5 >> task_test_6