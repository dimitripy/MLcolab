# main_server.py
from aiohttp import web
import json
from git_utils import clone_project_from_github
from script_executor import execute_script

# Request-Handler für Airflow-Aufträge
async def handle_request(request):
    try:
        data = await request.json()
        project_name = data.get('project')
        branch = data.get('branch', 'main')  # Verwende 'main', wenn kein Branch übergeben wurde
        script_name = data.get('script')
        parameters = data.get('parameters', [])

        if not all([project_name, branch, script_name]):
            return web.Response(status=400, text="Fehlende Projektinformationen (Projekt, Branch, Skript).")

        # Überprüfen und Klonen/Aktualisieren des Projekts
        project_path = f"/path/to/projects/{project_name}/{branch}" #TODO Projektpfad auslagern
        success, message = clone_project_from_github(project_name, branch, project_path)
        if not success:
            return web.Response(status=500, text=f"Fehler beim Klonen/Aktualisieren des Projekts: {message}")
        
        # Ausführen des Skripts und Rückmeldung
        success, output = await execute_script(project_path, script_name, parameters)
        if success:
            return web.Response(text=f"Skript erfolgreich ausgeführt. Ausgabe:\n{output}")
        else:
            return web.Response(status=500, text=f"Fehler bei der Skriptausführung: {output}")
    
    except json.JSONDecodeError:
        return web.Response(status=400, text="Ungültiges JSON im Request.")
    except Exception as e:
        return web.Response(status=500, text=f"Interner Fehler: {str(e)}")

# Initialisiere den Webserver
async def init_app():
    app = web.Application()
    app.router.add_post('/trigger', handle_request)
    return app

async def main():
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 4041)
    await site.start()
    print("Server läuft auf http://127.0.0.1:4041")
