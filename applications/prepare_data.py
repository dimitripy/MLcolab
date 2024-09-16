# prepare_data.py
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Konfiguration laden
with open('config.json', 'r') as f:
    config = json.load(f)

# Spark Session erstellen
spark = SparkSession.builder \
    .appName("DataPreparation") \
    .enableHiveSupport() \
    .getOrCreate()

# Daten aus Hive laden basierend auf der Konfiguration
input_table = config['data_preparation']['input_table']
output_table = config['data_preparation']['output_table']
raw_data = spark.sql(f"SELECT * FROM {input_table}")

# Datenverarbeitung
processed_data = raw_data \
    .filter(col("feature1").isNotNull()) \
    .withColumn("feature2", col("feature2").cast("double"))

# Verarbeitungsergebnisse in Hive speichern
processed_data.write.mode("overwrite").saveAsTable(output_table)

spark.stop()
