import socket
import requests
import os

# Configuration des services à vérifier
SERVICES = {
    "Dify (Moteur d'IA)": {"host": "localhost", "port": 8088, "url": "http://localhost:8088"},
    "n8n (Orchestrateur)": {"host": "localhost", "port": 5678, "url": "http://localhost:5678"},
    "Whisper (Transcription)": {"host": "localhost", "port": 8000, "url": "http://localhost:8000/v1/models"},
    "Ollama (Modèles Locaux)": {"host": "localhost", "port": 11434, "url": "http://localhost:11434"},
    "Interface SaaS (Cockpit)": {"host": "localhost", "port": 5000, "url": "http://localhost:5000"}
}

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

def check_url(url):
    try:
        response = requests.get(url, timeout=2)
        return response.status_code < 500
    except:
        return False

def run_diagnostic():
    print("\n" + "="*50)
    print("🔍 CHECK-UP SANTÉ : ATELIER AGENTIQUE ÉDITORIAL")
    print("="*50 + "\n")
    
    all_ok = True
    for name, config in SERVICES.items():
        port_open = check_port(config["host"], config["port"])
        
        if port_open:
            status = "✅ OPÉRATIONNEL"
            # Une vérification HTTP plus fine pour Dify et n8n
            if not check_url(config["url"]):
                status = "⚠️ PORT OUVERT MAIS NE RÉPOND PAS (HTTP ERROR)"
                all_ok = False
        else:
            status = "❌ ARRÊTÉ (PORT FERMÉ)"
            all_ok = False
            
        print(f"{name:<25} : {status}")

    print("\n" + "="*50)
    if all_ok:
        print("✨ TOUT EST PRÊT ! Vous pouvez commencer à travailler.")
    else:
        print("🛠️ ACTION REQUISE : Relancez les services manquants.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_diagnostic()
