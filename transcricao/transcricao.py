# transcricao.py
# Funções relacionadas à captura e transcrição do áudio

import whisper
import pyaudio
import numpy as np
import time
import json # Adicionado para usar json.dumps

# Importa as configurações do arquivo config.py
import config
# A função 'esta_ativo' foi removida do import, pois não será mais usada.
from utils import limpar_texto
from traducao import traduzir_texto

# Inicializa o modelo Whisper
try:
    model = whisper.load_model(config.MODELO_WHISPER)
    print(f"✅ Modelo Whisper '{config.MODELO_WHISPER}' carregado com sucesso.")
except Exception as e:
    print(f"❌ Erro ao carregar o modelo Whisper '{config.MODELO_WHISPER}': {e}")
    print("Certifique-se de que o modelo foi baixado ou que o nome está correto.")
    exit() # Sai do programa se o modelo não puder ser carregado

def iniciar_stream_audio(canal_de_audio):
    """
    Inicializa e retorna o stream de áudio do PyAudio.
    """
    p = pyaudio.PyAudio()
    try:
        # Tenta abrir o stream com o canal de áudio especificado
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024,
                        input_device_index=canal_de_audio)
        print(f"🎙️ Stream de áudio iniciado no dispositivo de índice {canal_de_audio}.")
        return p, stream
    except Exception as e:
        print(f"❌ Erro ao iniciar o stream de áudio no dispositivo {canal_de_audio}: {e}")
        print("Verifique se o índice do dispositivo de áudio em config.py está correto.")
        print("Use 'python main.py' para listar os dispositivos disponíveis.")
        return None, None

def capturar_e_transcrever(p_audio, stream_audio, send_to_websocket_clients):
    """
    Loop principal para captura, transcrição e envio de áudio.
    """
    print(f"📝 Pronto para transcrever. Controle a ativação via 'config.py' (TRANSCRICAO_ATIVA).")
    
    while True:
        # Verifica diretamente a variável de configuração
        if not config.TRANSCRICAO_ATIVA:
            time.sleep(1) # Espera 1 segundo se a transcrição estiver desativada
            continue

        if stream_audio is None or not stream_audio.is_active():
            print("❗ Stream de áudio inativo ou não inicializado. Tentando reiniciar...")
            p_audio, stream_audio = iniciar_stream_audio(config.CANAL_DE_AUDIO)
            if stream_audio is None:
                time.sleep(5) # Espera antes de tentar novamente
                continue

        frames = []
        try:
            # Captura aproximadamente 1 segundo de áudio (16000 Hz / 1024 buffer = ~15.6 frames por segundo)
            # 16 frames * 1024 buffer = ~1 segundo de áudio
            for _ in range(int(16000 / 1024)): 
                data = stream_audio.read(1024, exception_on_overflow=False)
                frames.append(np.frombuffer(data, dtype=np.int16))
        except IOError as e:
            print(f"Erro de I/O no stream de áudio: {e}")
            print("Provavelmente buffer overflow. Reduzindo a frequência de leitura ou ajustando buffer.")
            time.sleep(0.5) # Pequena pausa para tentar recuperar
            continue
        except Exception as e:
            print(f"Erro inesperado na captura de áudio: {e}")
            time.sleep(1)
            continue

        if not frames:
            continue

        audio_np = np.concatenate(frames).astype(np.float32) / 32768.0 # Normaliza para float32

        try:
            result = model.transcribe(audio_np, language=config.IDIOMA_ORIGEM)
            texto_original = limpar_texto(result["text"])
        except Exception as e:
            print(f"Erro durante a transcrição: {e}")
            texto_original = "" # Limpa o texto em caso de erro

        if texto_original:
            texto_para_enviar = {"original": texto_original}
            
            if config.TRADUZIR_PARA_INGLES:
                texto_traduzido = traduzir_texto(texto_original, config.IDIOMA_ORIGEM, config.IDIOMA_DESTINO)
                texto_para_enviar["traduzido"] = texto_traduzido
                
                if config.MODO_BILINGUE:
                    # Se modo bilíngue, envia ambos na mesma string
                    texto_final = f"{texto_original} ({texto_traduzido})"
                else:
                    # Se não, envia apenas o traduzido
                    texto_final = texto_traduzido
            else:
                # Se tradução desativada, envia apenas o original
                texto_final = texto_original

            print(f"📝 [ORIGINAL]: {texto_original}")
            if config.TRADUZIR_PARA_INGLES:
                print(f"🌐 [TRADUZIDO]: {texto_traduzido}")
            
            # Envia o texto final para os clientes WebSocket
            send_to_websocket_clients(json.dumps(texto_para_enviar))

            # O log ainda salva o texto final conforme configurado
            with open(config.ARQUIVO_LOG, "a", encoding="utf-8") as log:
                log.write(texto_final + "\n")
        
        time.sleep(0.1) # Pequena pausa para evitar uso excessivo da CPU

