# save_predictions_to_cassandra.py
from pyspark.sql import SparkSession
from cassandra.cluster import Cluster

# Spark Session erstellen
spark = SparkSession.builder \
    .appName("SavePredictionsToCassandra") \
    .getOrCreate()

# Verbindung zu Cassandra herstellen
cluster = Cluster(['127.0.0.1'])  # Cassandra-Host-IP-Adresse anpassen
session = cluster.connect('model_results')  # 'model_results' ist der Keyspace in Cassandra

# Beispiel: Vorhersagen aus Spark laden
predictions = spark.sql("SELECT * FROM model_predictions")  # 'model_predictions' ist die Tabelle mit den Vorhersagen

# Vorhersagen in Cassandra speichern
for row in predictions.collect():
    session.execute(
        """
        INSERT INTO predictions (id, feature1, feature2, prediction)
        VALUES (%s, %s, %s, %s)
        """,
        (row.id, row.feature1, row.feature2, row.prediction)
    )

# Verbindung schließen
cluster.shutdown()
spark.stop()
