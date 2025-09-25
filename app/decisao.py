import requests
from datetime import datetime
from .modelos import ProcessoBase
from .preprocessador import converter_para_minimo
from .llm import decidir_com_llm

import os
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

def _formatar_datas(obj):
    if isinstance(obj, datetime):
        return obj.isoformat().replace("+00:00", "Z")
    if isinstance(obj, dict):
        return {k: _formatar_datas(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_formatar_datas(v) for v in obj]
    return obj

def analisar_processo(json_entrada: dict) -> dict:
    base = ProcessoBase(**json_entrada)
    minimo = converter_para_minimo(base)
    decisao = decidir_com_llm(minimo)

    resposta = {
        "numeroProcesso": minimo.numero_processo,
        "classe": minimo.classe,
        "orgaoJulgador": minimo.orgao_julgador,
        "ultimaDistribuicao": minimo.ultima_distribuicao,
        "valorCausa": minimo.valor_causa,
        "assunto": minimo.assunto,
        "segredoJustica": minimo.segredo_justica,
        "justicaGratuita": minimo.justica_gratuita,
        "siglaTribunal": minimo.sigla_tribunal,
        "esfera": minimo.esfera,
        "valorCondenacao": minimo.valor_condenacao,
        "documentos": minimo.documentos,
        "honorarios": minimo.honorarios or {},
        "resultado": decisao.resultado,
        "justificativa": decisao.justificativa,
        "citacoes": decisao.citacoes,
    }

    resposta_formatada = _formatar_datas(resposta)

    # 🔹 Envia resultado para o n8n
    try:
      r = requests.post(WEBHOOK_URL, json=resposta_formatada, timeout=5)
      print(f"[n8n] Status: {r.status_code}, Response: {r.text}")  # debug
    except Exception as e:
      print(f"[n8n] Erro ao enviar webhook: {e}")

    return resposta_formatada
