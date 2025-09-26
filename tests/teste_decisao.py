"""
📌 Função deste arquivo:
Validar a API do verificador de processos, enviando arquivos de teste em JSON
para o endpoint /analisar e exibindo a saída formatada.

------------------------------------------------------------------------------------------------------------------------
Principais responsabilidades:

Configuração da URL de teste:
➡ Define URL = "http://127.0.0.1:8000/analisar", apontando para o servidor FastAPI local.

Função testar_arquivo:
➡ Lê um arquivo JSON de processos.
➡ Envia o conteúdo para o endpoint via requests.post.
➡ Exibe o resultado no console em formato legível.
➡ Se a resposta não for 200 OK, dispara exceção (raise_for_status).

Execução principal:
➡ Testa dois cenários:
"tests/teste_unico.json" → arquivo com um único processo.
"tests/teste_lista_11.json" → arquivo com lista de processos.






"""



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
