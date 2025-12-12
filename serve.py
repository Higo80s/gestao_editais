from waitress import serve
from app import app
import socket

# Get local IP to print it
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f" * Servidor de Producao (Waitress) Iniciado!")
print(f" * Acessivel em: http://127.0.0.1:5000")
print(f" * Acessivel na rede: http://{local_ip}:5000")
print(" * Janela do navegador abrira em instantes...")

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
