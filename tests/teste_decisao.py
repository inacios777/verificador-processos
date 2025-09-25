# teste_decisao.py
import json
import requests

URL = "http://127.0.0.1:8000/analisar"

def testar_arquivo(arquivo: str):
    """Lê um JSON de processos e envia para a API"""
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    resp = requests.post(URL, json=dados)
    resp.raise_for_status()

    print(f"\n=== Teste ({arquivo}) ===")
    print(resp.text)


if __name__ == "__main__":
    # Arquivos de teste
    testar_arquivo("tests/teste_unico.json")
    testar_arquivo("tests/teste_lista_11.json")
