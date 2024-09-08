# train_model.py
import json
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
import mlflow
import mlflow.spark

# Konfiguration laden
with open('config.json', 'r') as f:
    config = json.load(f)

# Spark Session erstellen
spark = SparkSession.builder \
    .appName("ModelTraining") \
    .enableHiveSupport() \
    .getOrCreate()

# Daten laden und vorbereiten
input_table = config['data_preparation']['output_table']
df = spark.sql(f"SELECT * FROM {input_table}")

# Features und Label aus der Konfiguration
features = config['model_training']['features']
label = config['model_training']['label']
assembler = VectorAssembler(inputCols=features, outputCol="features")
transformed_df = assembler.transform(df)

# Train-Test-Split basierend auf der Konfiguration
test_split = config['model_training']['test_split']
(train_data, test_data) = transformed_df.randomSplit([1 - test_split, test_split])

# Modell initialisieren und trainieren
lr = LogisticRegression(featuresCol="features", labelCol=label)
model = lr.fit(train_data)

# Bewertung und Logging
with mlflow.start_run():
    mlflow.log_param("model_type", "Logistic Regression")
    accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(test_data.count())
    mlflow.log_metric("accuracy", accuracy)
    mlflow.spark.log_model(model, "model")

spark.stop()
