# ngrok_utils.py
import asyncio
from pyngrok import ngrok

async def start_ngrok(authtoken, port):
    ngrok.kill()  # Beendet ngrok, falls es bereits läuft
    await run_process(['ngrok', 'config', 'add-authtoken', authtoken])
    await run_process(['ngrok', 'http', '--log', 'stderr', str(port), '--host-header', f'localhost:{port}'])

async def run_process(cmd):
    p = await asyncio.subprocess.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def pipe(lines):
        async for line in lines:
            print(line.strip().decode('utf-8'))

    await asyncio.gather(pipe(p.stdout), pipe(p.stderr))
