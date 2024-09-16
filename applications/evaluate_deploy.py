# evaluate_deploy.py
import json
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import mlflow
import mlflow.spark

# Konfiguration laden
with open('config.json', 'r') as f:
    config = json.load(f)

# Spark Session erstellen
spark = SparkSession.builder \
    .appName("ModelEvaluationAndDeployment") \
    .getOrCreate()

# Modell aus der Konfiguration laden
model_uri = config['model_evaluation']['model_uri']
model = mlflow.spark.load_model(model_uri)

# Testdaten laden
input_table = config['data_preparation']['output_table']
test_data = spark.sql(f"SELECT * FROM {input_table}")

# Modell bewerten
predictions = model.transform(test_data)
evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction")
accuracy = evaluator.evaluate(predictions)

# Ergebnisse loggen
mlflow.log_metric("evaluation_accuracy", accuracy)

print(f"Evaluated model accuracy: {accuracy}")

spark.stop()
