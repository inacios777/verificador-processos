# app/main.py
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
