# main.py
# Arquivo principal que inicializa o sistema de transcrição e o servidor WebSocket.

from flask import Flask, render_template
from flask_sockets import Sockets
import threading
import json
import time

# Importa as configurações e funções dos outros módulos
import config
from utils import listar_dispositivos_audio
from transcricao import iniciar_stream_audio, capturar_e_transcrever

app = Flask(__name__, template_folder='templates', static_folder='static')
sockets = Sockets(app)

# Lista para armazenar os clientes WebSocket conectados
connected_clients = []

@app.route('/')
def index():
    """Rota principal que redireciona para a página de rodapé."""
    return render_template('rodape.html')

@app.route('/fullscreen')
def fullscreen():
    """Rota para a página de transcrição em tela cheia."""
    return render_template('fullscreen.html')

@app.route('/rodape')
def rodape():
    """Rota para a página de transcrição no rodapé."""
    return render_template('rodape.html')

@sockets.route('/ws')
def websocket_connection(ws):
    """
    Gerencia as conexões WebSocket.
    Adiciona o cliente à lista de conectados e o remove quando a conexão é fechada.
    """
    print(f"🔗 Cliente WebSocket conectado: {ws.environ['REMOTE_ADDR']}")
    connected_clients.append(ws)
    
    while not ws.closed:
        try:
            # Mantém a conexão aberta, lendo mensagens (opcional, mas bom para keep-alive)
            message = ws.receive()
            if message:
                print(f"Mensagem recebida do cliente WebSocket: {message}")
        except Exception as e:
            print(f"Erro no WebSocket: {e}")
            break # Sai do loop em caso de erro

    print(f"💔 Cliente WebSocket desconectado: {ws.environ['REMOTE_ADDR']}")
    if ws in connected_clients:
        connected_clients.remove(ws)

def send_to_websocket_clients(message):
    """
    Envia uma mensagem para todos os clientes WebSocket conectados.
    """
    # Cria uma cópia da lista para evitar problemas se a lista for modificada durante a iteração
    for client in list(connected_clients): 
        try:
            client.send(message)
        except Exception as e:
            print(f"Erro ao enviar mensagem para cliente WebSocket: {e}")
            # Remove clientes que falharam no envio (provavelmente desconectados)
            if client in connected_clients:
                connected_clients.remove(client)

def iniciar_servidor_flask():
    """
    Inicia o servidor Flask para servir as páginas HTML e o WebSocket.
    """
    print(f"🌐 Servidor Web Flask iniciado em http://localhost:{config.PORTA_WEB_SERVER}")
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', config.PORTA_WEB_SERVER), app, handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    # 1. Lista os dispositivos de áudio disponíveis
    listar_dispositivos_audio()

    # 2. Inicia o servidor Flask (incluindo WebSocket) em uma thread separada
    flask_thread = threading.Thread(target=iniciar_servidor_flask)
    flask_thread.daemon = True # Permite que a thread seja encerrada quando o programa principal termina
    flask_thread.start()
    
    time.sleep(1) # Pequena pausa para garantir que o servidor Flask inicie

    # 3. Inicializa o stream de áudio
    p_audio, stream_audio = iniciar_stream_audio(config.CANAL_DE_AUDIO)

    if p_audio and stream_audio:
        # 4. Inicia o loop de captura e transcrição
        # Passa a função send_to_websocket_clients para o módulo de transcrição
        # A verificação de TRANSCRICAO_ATIVA agora é feita dentro de capturar_e_transcrever
        capturar_e_transcrever(p_audio, stream_audio, send_to_websocket_clients)
    else:
        print("❌ Não foi possível iniciar a transcrição devido a problemas com o stream de áudio.")
        print("Por favor, verifique as configurações e tente novamente.")

