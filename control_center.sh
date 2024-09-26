#!/bin/bash

# Gemeinsame Funktionen einbinden
source "$(dirname "${BASH_SOURCE[0]}")/Comms/common_functions.sh"

# .env Datei einlesen
ENV_FILE="$(dirname "${BASH_SOURCE[0]}")/.env"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo ".env Datei $ENV_FILE nicht gefunden!"
    exit 1
fi

# Verzeichnisse und Dateien definieren
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLABSIDE_DIR="$SCRIPT_DIR/ColabSide"  # Pfad zum ColabSide-Verzeichnis
DAGS_DIR="$SCRIPT_DIR/dags"
INTEGRATION_SCRIPT="$SCRIPT_DIR/Comms/intigration.sh"  # Pfad zum intigration.sh Skript
CUSTOM_FUNCTIONS_DIR="$SCRIPT_DIR/Customs"  # Pfad zum CustomFunctions-Verzeichnis

# Überprüfe und installiere erforderliche Python-Pakete
install_python_packages() {
    log "$PROJECT_NAME" "Überprüfe und installiere erforderliche Python-Pakete..."

    REQUIRED_PKG=("pydrive" "gitpython")
    for PKG in "${REQUIRED_PKG[@]}"; do
        if ! python3 -c "import $PKG" &> /dev/null; then
            log "$PROJECT_NAME" "Installiere $PKG..."
            pip3 install $PKG
        else
            log "$PROJECT_NAME" "$PKG ist bereits installiert."
        fi
    done

    log "$PROJECT_NAME" "Alle erforderlichen Python-Pakete sind installiert."
}

# Google Drive Authentifizierung und Projektverzeichnis erstellen
setup_colabside() {
    log "$PROJECT_NAME" "Richte ColabSide-Verzeichnis ein..."

    python3 "$CUSTOM_FUNCTIONS_DIR/import_colabside.py" "$PROJECT_NAME" "$REPO_URL" "$BRANCH" "$NGROK_AUTHTOKEN" "$PORT"

    log "$PROJECT_NAME" "ColabSide-Verzeichnis eingerichtet."
}

# Initialisierungsfunktion
initialize_project() {
    log "$PROJECT_NAME" "Starte Initialisierung des Projekts..."

    # Registriere in der zentralen Registry und trigger den Sync-DAG
    if [ -f "$INTEGRATION_SCRIPT" ]; then
        bash "$INTEGRATION_SCRIPT" "$PROJECT_NAME" \
            "dag_path=$DAGS_DIR"
    else
        echo "intigration.sh Skript nicht gefunden unter $INTEGRATION_SCRIPT"
        exit 1
    fi

    # Installiere erforderliche Python-Pakete
    install_python_packages

    # Richte ColabSide-Verzeichnis ein
    setup_colabside

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
        # Optionaler Ort um den Test DAG zu triggern
        ;;
    9)
        log "$PROJECT_NAME" "Hard Reset wird durchgeführt..."
        # Hier wird der Hard Reset durchgeführt, indem alle bisherigen Daten gelöscht werden
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