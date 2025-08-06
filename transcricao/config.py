# config.py
# Variáveis de controle para o sistema de transcrição e tradução

# --- Configurações de Ativação ---
TRANSCRICAO_ATIVA = True  # Define se a transcrição deve ser iniciada automaticamente
TRADUZIR_PARA_INGLES = True # Ativa ou desativa a tradução para o inglês
MODO_BILINGUE = False     # Se True, exibe tanto o texto original quanto o traduzido (requer TRADUZIR_PARA_INGLES = True)

# --- Configurações de Áudio ---
# O índice do dispositivo de áudio a ser usado para captura.
# Execute 'python main.py' para listar os dispositivos disponíveis e seus índices.
# Exemplo: Se o dispositivo desejado for o 3, defina CANAL_DE_AUDIO = 3
CANAL_DE_AUDIO = 0 # Defina 0 para o dispositivo padrão, ou o índice específico

# --- Configurações do Modelo Whisper ---
# Modelos disponíveis: 'tiny', 'base', 'small', 'medium', 'large'
# Modelos maiores são mais precisos, mas mais lentos e exigem mais recursos.
MODELO_WHISPER = "tiny"

# --- Configurações de Idioma ---
# Idioma do áudio de origem (ex: "pt", "en", "es", "fr")
IDIOMA_ORIGEM = "pt"
# Idioma para o qual o texto será traduzido (ex: "en", "pt", "es", "fr")
IDIOMA_DESTINO = "en"

# --- Configurações de Log e Status ---
# Arquivo onde as transcrições serão salvas
ARQUIVO_LOG = "transcricao.log"
# Arquivo de controle para ativar/desativar a transcrição em tempo real (conteúdo 'on' ou 'off')
ARQUIVO_STATUS = "status.txt"

# --- Configurações do Servidor WebSocket ---
# Endereço do servidor WebSocket que enviará as transcrições para as páginas HTML
ENDERECO_WS = "ws://localhost:3001/ws" # O caminho '/ws' é importante para a conexão
PORTA_WEB_SERVER = 3000 # Porta para as páginas HTML (Flask)
PORTA_WEBSOCKET = 3001 # Porta para o servidor WebSocket (Flask-Sockets)
