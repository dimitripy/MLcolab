# track_model.py

import mlflow
import mlflow.spark
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator

def track_model():
    # MLflow Tracking Server URI setzen
    mlflow.set_tracking_uri("http://localhost:5000")  # Passe die URI an deinen MLflow Server an
    mlflow.set_experiment("ML-Model-Tracking")  # Experiment-Name anpassen oder erstellen

    # Start einer neuen MLflow-Run
    with mlflow.start_run(run_name="TrainingRun") as run:
        # Modellparameter loggen
        mlflow.log_param("algorithm", "RandomForest")
        mlflow.log_param("num_trees", 50)
        mlflow.log_param("max_depth", 10)
        
        # Spark Session erstellen
        spark = SparkSession.builder \
            .appName("ModelTracking") \
            .getOrCreate()
        
        # Beispielhafte Modellbewertung (anpassen an deine Daten)
        predictions = spark.sql("SELECT * FROM model_predictions")  # Beispielhafter SQL-Abfrage für Vorhersagen
        evaluator = RegressionEvaluator(labelCol="true_label", predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        
        # Metriken loggen
        mlflow.log_metric("rmse", rmse)
        
        # Modell speichern
        model_path = "/path/to/saved_model"  # Anpassen auf den tatsächlichen Speicherort des Modells
        mlflow.spark.log_model(spark_model=model_path, artifact_path="model", registered_model_name="RandomForestModel")
        
        # Zusätzliche Artefakte loggen
        mlflow.log_artifact("/path/to/feature_importance_plot.png")  # Beispiel: Artefakt (Plot)
        mlflow.log_artifact("/path/to/config.yaml")  # Beispiel: Konfigurationsdatei

        # Abschluss des Runs
        mlflow.end_run()
