#!/bin/bash
#regitry.sh

# Verzeichnis und Pfad zur zentralen Registry-Datei
REGISTRY_DIR="/etc/airflow"
REGISTRY_FILE="$REGISTRY_DIR/airflow_dag_registry.yaml"

register_in_registry() {
  PROJECT_NAME=$1
  shift  # Entferne den ersten Parameter (Projektname)

  echo "Registriere Unterprojekt in der zentralen DAG-Registry..."

  # Überprüfen, ob das Registry-Verzeichnis existiert
  if [ ! -d "$REGISTRY_DIR" ]; then
    echo "Registry-Verzeichnis $REGISTRY_DIR existiert nicht. Erstelle es..."
    sudo mkdir -p "$REGISTRY_DIR"
    sudo chmod 777 "$REGISTRY_DIR"  # Alle Benutzer dürfen in das Verzeichnis schreiben
  fi

  # Überprüfen, ob die Registry-Datei existiert
  if [ ! -f "$REGISTRY_FILE" ]; then
    echo "Registry-Datei $REGISTRY_FILE existiert nicht. Erstelle sie..."
    sudo touch "$REGISTRY_FILE"
    sudo chmod 666 "$REGISTRY_FILE"  # Alle Benutzer dürfen in die Datei schreiben
    echo "# Globale DAG Registry File" | sudo tee -a "$REGISTRY_FILE" > /dev/null
    echo "# List of registered submodules and their DAG paths" | sudo tee -a "$REGISTRY_FILE" > /dev/null
  fi

  # Projekt zur Registry hinzufügen oder aktualisieren
  for param in "$@"; do
    key=$(echo "$param" | cut -d= -f1)
    value=$(echo "$param" | cut -d= -f2)
    sudo yq eval ".projects[\"$PROJECT_NAME\"].$key = \"$value\"" -i "$REGISTRY_FILE"
  done

  echo "Unterprojekt $PROJECT_NAME wurde erfolgreich in die Registry eingetragen."
}

trigger_sync_dag() {
  echo "Trigger den 'sync_all_dags' DAG in Airflow im Docker-Container..."

  # Name des Docker Compose Service (anpassen, falls anders)
  SERVICE_NAME="mlcsope-airflow-scheduler-1"

  # Überprüfen, ob der Service läuft (Docker Compose sollte im Verzeichnis sein)
  if ! docker ps | grep -q "$SERVICE_NAME"; then
    echo "Der Service '$SERVICE_NAME' läuft nicht. Bitte stelle sicher, dass der Airflow-Container läuft und versuche es erneut."
    exit 1
  fi

  # Trigger den DAG innerhalb des Containers
  docker exec -it "$SERVICE_NAME" airflow dags trigger sync_all_dags

  if [ $? -eq 0 ]; then
    echo "Der DAG 'sync_all_dags' wurde erfolgreich im Docker-Container getriggert."
  else
    echo "Fehler beim Triggern des DAGs 'sync_all_dags' im Docker-Container."
  fi
}

show_registry_path() {
  echo "Der Pfad zur Registry-Datei ist: $REGISTRY_FILE"
}

# Überprüfen, ob mindestens ein Argument übergeben wurde
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <PROJECT_NAME> [KEY=VALUE]..."
  exit 1
fi

# Aufruf der Funktion zur Registrierung
register_in_registry "$@"

# Trigger den Sync-DAG nach der Registrierung
trigger_sync_dag

# Zeige den Pfad zur Registry-Datei
show_registry_path