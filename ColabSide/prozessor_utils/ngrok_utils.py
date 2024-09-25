# ngrok_utils.py
import asyncio
from pyngrok import ngrok



async def run_process(cmd):
    print('>>> starting', *cmd)
    p = await asyncio.subprocess.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def pipe(lines):
        async for line in lines:
            print(line.strip().decode('utf-8'))

    await asyncio.gather(
        pipe(p.stdout),
        pipe(p.stderr),
    )

async def start_ngrok(authtoken, port):
    try:
        ngrok.kill()  # Beendet ngrok, falls es bereits läuft
        await run_process(['ngrok', 'config', 'add-authtoken', authtoken])
        public_url = ngrok.connect(port).public_url 
        print(f"ngrok-Tunnel geöffnet unter {public_url}")
        print("Test mit:")
        print(f"curl {public_url}/health")
        
    except Exception as e:
        print(f"Fehler beim Starten von ngrok: {str(e)}")

        
        
'''
easy mode

async def start_ngrok(authtoken, port):
    try:
        ngrok.kill()  # Beendet ngrok, falls es bereits läuft
        ngrok.set_auth_token(authtoken)
        public_url = ngrok.connect(port).public_url 
        print(f"ngrok-Tunnel geöffnet unter {public_url}")
        print("Test mit:")
        print(f"curl {public_url}/health")
        
    except Exception as e:
        print(f"Fehler beim Starten von ngrok: {str(e)}")
'''
