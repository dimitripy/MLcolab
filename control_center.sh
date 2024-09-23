/home/ageq/Git_Projects/MLcoworker/ColabSide/.env#!/bin/bash

# Gemeinsame Funktionen einbinden
source "$(dirname "${BASH_SOURCE[0]}")/Comms/common_functions.sh"

PROJECT_NAME="mlcoworker"

# Verzeichnisse und Dateien definieren
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/ColabSide/.env"  # Pfad zur .env Datei
COLABSIDE_DIR="$SCRIPT_DIR/ColabSide"  # Pfad zum ColabSide-Verzeichnis
CONFIG_FILE="$SCRIPT_DIR/../dags/config.json"  # Pfad zur config.json Datei
DAGS_DIR="$SCRIPT_DIR/dags"

# .env Datei erstellen
create_env_file() {
    local env_file=ENV_FILE
    cat <<EOF > "$env_file"
NGROK_AUTHTOKEN=
PROJECT_PATH_TEMPLATE=
PORT=5000
EOF
    echo ".env Datei wurde erfolgreich erstellt unter $env_file"
}


# Initialisierungsfunktion
initialize_project() {
    log "$PROJECT_NAME" "Starte Initialisierung des Projekts..."

    # Erstelle .env Datei im ColabSide-Verzeichnis
    create_env_file "$ENV_FILE"

    # Registriere in der zentralen Registry
    register_in_registry "$PROJECT_NAME" "$DAGS_DIR" 

    # Trigger den Sync-DAG in Airflow
    trigger_sync_dag

    # Richte ColabSide-Verzeichnis ein
    #TODO erstelle die Funktion setup_colabside
    setup_colabside "$PROJECT_NAME" "$COLABSIDE_DIR"

    log "$PROJECT_NAME" "Initialisierung des Projekts abgeschlossen."
}

# Menü für Benutzerinteraktion
echo "Bitte wähle eine Option:"
echo "1 - Projekt initialisieren"
echo "5 - Pingpong-Test"
echo "9 - Hard Reset (alles löschen und neu erstellen)"
echo "0 - Beenden"

read -p "Eingabe: " choice
case $choice in
    1)
        initialize_project
        ;;
    5)
        log "$PROJECT_NAME" "Dummy-Test wird durchgeführt..."
        # Optonaler Ort um den Test DAG zu triggern

        ;;
    9)
        log "$PROJECT_NAME" "Hard Reset wird durchgeführt..."
        # Hier wird der Hard Reset durchgeführt, indem alle bisherigen Daten gelöscht werden
        #TODO erstelle die Funktion hard_reset
        rm -rf "$COLABSIDE_DIR/.env"
        rm -rf "$COLABSIDE_DIR"
        initialize_project
        ;;
    0)
        echo "Beenden..."
        exit 0
        ;;
    *)
        echo "Ungültige Eingabe. Bitte wähle eine gültige Option."
        ;;
esac