# traducao.py
# Funções de tradução para o sistema de transcrição

import requests
import json
import time

def traduzir_texto(texto, idioma_origem, idioma_destino):
    """
    Traduz um texto usando um serviço de tradução local (ex: LibreTranslate).
    Retorna o texto traduzido ou o texto original em caso de erro.
    """
    # URL padrão para um serviço LibreTranslate rodando localmente na porta 5000
    traducao_url = "http://localhost:5000/translate"
    
    try:
        payload = {
            "q": texto,
            "source": idioma_origem,
            "target": idioma_destino,
            "format": "text"
        }
        headers = {"Content-Type": "application/json"}
        
        resposta = requests.post(traducao_url, json=payload, headers=headers, timeout=5)
        resposta.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        
        dados = resposta.json()
        if "translatedText" in dados:
            return dados["translatedText"]
        else:
            print(f"Erro na resposta da tradução: {dados}")
            return texto # Fallback: retorna o texto original
            
    except requests.exceptions.ConnectionError:
        print(f"Erro de conexão com o servidor de tradução em {traducao_url}. Ele está rodando?")
        print("Certifique-se de que um serviço como o LibreTranslate está ativo na porta 5000.")
        return texto # Fallback: retorna o texto original
    except requests.exceptions.Timeout:
        print("Tempo limite excedido ao conectar com o servidor de tradução.")
        return texto # Fallback: retorna o texto original
    except requests.exceptions.RequestException as e:
        print(f"Erro ao traduzir texto: {e}")
        return texto # Fallback: retorna o texto original
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON da resposta de tradução: {resposta.text}")
        return texto # Fallback: retorna o texto original

