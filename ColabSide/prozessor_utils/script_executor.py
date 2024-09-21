# script_executor.py
import asyncio
import os

async def execute_script(project_path, script_name, parameters):
    script_path = os.path.join(project_path, script_name)
    if not os.path.exists(script_path):
        return False, f"Skript '{script_name}' nicht gefunden im Projektpfad '{project_path}'"
    
    # Führe das Skript mit den Parametern aus
    cmd = ['python3', script_path] + parameters
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return True, stdout.decode()
    else:
        return False, stderr.decode()
