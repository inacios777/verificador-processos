"""

📌 Função deste arquivo:
Definir a API FastAPI que expõe os endpoints do verificador de processos.
Permite enviar um ou vários processos para análise e obter como resposta tanto texto formatado quanto JSON estruturado.

------------------------------------------------------------------------------------------------------------------------
Principais responsabilidades:

Configuração da API:
➡ Instancia um app FastAPI com título "Verificador de Processos".

Endpoint /analisar (texto legível):
➡ Entrada: um único processo (dict) ou uma lista de processos.
➡ Para cada processo, chama analisar_processo.
➡ Retorna saída em texto formatado, usando formatar_resultados.
➡ Resposta com PlainTextResponse para facilitar visualização em testes.

Endpoint /analisar_json (contratual):
➡ Entrada: igual ao /analisar (um ou vários processos).
➡ Retorna saída em JSON estruturado, pronto para consumo em integrações.

Endpoint /health:
➡ Retorna {"status": "ok"}.
➡ Usado para monitoramento e checagem de disponibilidade do serviço.

Tratamento de erros:
➡ Em ambos os endpoints principais, captura exceções e retorna HTTP 400 com detalhe do erro.

"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Union, List, Dict

from app.decisao import analisar_processo
from app.formatador import formatar_resultados

app = FastAPI(title="Verificador de Processos")

@app.post("/analisar", response_class=PlainTextResponse)
def analisar_endpoint(json_entrada: Union[Dict, List[Dict]]):
    """Retorna TEXTO formatado (legível)."""
    try:
        if isinstance(json_entrada, dict):
            resultados = [analisar_processo(json_entrada)]
        else:
            resultados = [analisar_processo(proc) for proc in json_entrada]
        return formatar_resultados(resultados)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analisar_json")
def analisar_json(json_entrada: Union[Dict, List[Dict]]):
    """Retorna JSON estruturado (contratual)."""
    try:
        if isinstance(json_entrada, dict):
            return analisar_processo(json_entrada)
        return [analisar_processo(proc) for proc in json_entrada]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
