#flask_server.py
from flask import Flask, request, jsonify
import subprocess
from git_utils import clone_project_from_github
from script_executor import execute_script
import os
import asyncio

app = Flask(__name__)

@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.json
    project_name = data.get('project')
    branch = data.get('branch', 'main')
    script_name = data.get('script')
    parameters = data.get('parameters', [])

    if not all([project_name, branch, script_name]):
        return jsonify({'status': 'error', 'message': 'Fehlende Projektinformationen (Projekt, Branch, Skript).'}), 400

    try:
        project_path = os.getenv("PROJECT_PATH_TEMPLATE").format(project_name=project_name, branch=branch)
        success, message = clone_project_from_github(project_name, branch, project_path)
        if not success:
            return jsonify({'status': 'error', 'message': f'Fehler beim Klonen/Aktualisieren des Projekts: {message}'}), 500

        loop = asyncio.get_event_loop()
        success, output = loop.run_until_complete(execute_script(project_path, script_name, parameters))
        if success:
            return jsonify({'status': 'success', 'output': output})
        else:
            return jsonify({'status': 'error', 'message': f'Fehler bei der Skriptausführung: {output}'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Interner Fehler: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

def execute_script_sync(project_path, script_name, parameters):
    script_path = os.path.join(project_path, script_name)
    if not os.path.exists(script_path):
        return False, f"Skript '{script_name}' nicht gefunden im Projektpfad '{project_path}'"
    
    cmd = ['python3', script_path] + parameters
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)
    
'''
#Option nach freien Port zu suchen
import socket

def find_free_port(starting_port=5000):
    port = starting_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:  # Port ist frei
                return port
            port += 1  # Nächsten Port ausprobieren

def run_flask():
    port = find_free_port()  # Finde den nächsten freien Port
    app.run(port=port, debug=True)
'''
