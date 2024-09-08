from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Importiere die Funktion aus dem ausgelagerten Skript
from os import path
from applications.track_model import track_model  

# Definiere den DAG
with DAG(
    'automated_ml_workflow',
    start_date=datetime(2024, 9, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task: Datenvorbereitung
    load_and_prepare_data = SparkSubmitOperator(
        task_id='load_and_prepare_data',
        application=path.join("applications", "prepare_data.py"),
        conn_id='spark_default'
    )

    # Task: Modelltraining
    train_model = SparkSubmitOperator(
        task_id='train_model',
         application=path.join("applications", "train_model.py"),
        conn_id='spark_default'
    )

    # Task: Modelltracking (ausgelagerte Funktion)
    model_tracking = PythonOperator(
        task_id='model_tracking',
        python_callable=track_model  # Aufruf der Funktion aus track_model.py
    )

    # Task: Modellbewertung und Deployment
    evaluate_and_deploy_model = SparkSubmitOperator(
        task_id='evaluate_and_deploy_model',
         application=path.join("applications", "evaluate_deploy.py"),
        conn_id='spark_default'
    )

    # Task: Speichern der Vorhersagen in Cassandra
    save_predictions_to_cassandra = SparkSubmitOperator(
        task_id='save_predictions_to_cassandra',
         application=path.join("applications", "save_predictions.py"),
        conn_id='spark_default'
    )

    # Definiere die Task-Reihenfolge
    (
        load_and_prepare_data 
        >> train_model 
        >> model_tracking 
        >> evaluate_and_deploy_model 
        >> save_predictions_to_cassandra
    )
