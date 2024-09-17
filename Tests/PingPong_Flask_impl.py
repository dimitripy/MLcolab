from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Beispiel für eine Route, die ein Skript startet
@app.route('/run_script', methods=['POST'])
def run_script():
    # Übergabeparameter aus der Anfrage holen
    script_name = request.json.get('script_name')
    message = request.json.get('message')

    try:
        # Hier startest du das externe Python-Skript und übergibst den 'message'-Parameter
        result = subprocess.run(['python3', script_name, message], capture_output=True, text=True)

        # Prüfen, ob das Skript erfolgreich war
        if result.returncode == 0:
            return jsonify({'status': 'success', 'output': result.stdout})
        else:
            return jsonify({'status': 'error', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/ping', methods=['POST'])
def ping():
    message = request.json.get('message')
    if message == 'Ping':
        return jsonify({'response': 'Pong'})
    return jsonify({'response': 'Unknown command'})

@app.route('/dingdong', methods=['POST'])
def dingdong():
    message = request.json.get('message')
    if message == 'Ding':
        return jsonify({'response': 'Dong'})
    return jsonify({'response': 'Unknown command'})


if __name__ == '__main__':
    app.run(port=5000)


"""
#example_script.py
import sys

if __name__ == "__main__":
    # Übergabeparameter erhalten
    message = sys.argv[1]
    
    # Basierend auf dem Message-Parameter etwas tun
    if message == "Ping":
        print("Pong")
    elif message == "Ding":
        print("Dong")
    else:
        print(f"Unbekannte Nachricht: {message}")
        
### curl -X POST http://localhost:5000/run_script \
### -H "Content-Type: application/json" \
###-d '{"script_name": "example_script.py", "message": "Ping"}'

"""