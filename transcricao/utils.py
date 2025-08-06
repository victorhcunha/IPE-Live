# utils.py
# Funções auxiliares para o projeto de transcrição

import speech_recognition as sr
import os

def listar_dispositivos_audio():
    """
    Lista todos os dispositivos de microfone disponíveis no sistema
    e seus respectivos índices.
    """
    print("\n--- Dispositivos de Áudio Disponíveis ---")
    try:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{index}: {name}")
    except Exception as e:
        print(f"Erro ao listar dispositivos de áudio: {e}")
        print("Certifique-se de que o PyAudio e o SpeechRecognition estão instalados corretamente.")
    print("---------------------------------------\n")

# A função 'esta_ativo' foi removida, pois não será mais usada.

def limpar_texto(texto):
    """
    Função para limpar e formatar o texto transcrito.
    Pode ser expandida para remover pontuações indesejadas, padronizar maiúsculas/minúsculas, etc.
    """
    return texto.strip()

