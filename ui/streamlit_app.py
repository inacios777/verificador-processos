# streamlit_app.py
import json
import time
import os
from typing import Any, Union, List, Dict

import requests
import streamlit as st

# =========================
# Config
# =========================
DEFAULT_API = os.getenv("API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Verificador de Processos", page_icon="⚖️", layout="wide")

st.title("Verificador de Processos ⚖️")
st.caption("Envie um JSON (único processo ou lista) e veja a decisão/justificativa.")

api_base = st.text_input("URL da API", value=DEFAULT_API, help="Ex.: http://127.0.0.1:8000")
saida = st.radio("Formato de saída", ["Texto formatado (/analisar)", "JSON (/analisar_json)"], horizontal=True)
endpoint = "/analisar" if saida.startswith("Texto") else "/analisar_json"

if endpoint == "/analisar_json":
    pretty = st.toggle("Exibir no formato de texto do desafio (pretty=true)", value=False)
else:
    pretty = False

# =========================
# Entrada: colar JSON ou enviar arquivo
# =========================
tab1, tab2 = st.tabs(["📋 Colar JSON", "📁 Enviar arquivo .json"])

with tab1:
    body_text = st.text_area("Cole aqui o JSON", height=300, placeholder="{} ou [ {}, {}, ... ]")

with tab2:
    up = st.file_uploader("Selecione um arquivo .json", type=["json"])

def _carregar_payload() -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    if up is not None:
        return json.load(up)
    if body_text.strip():
        return json.loads(body_text)
    raise ValueError("Forneça o JSON colando no campo de texto ou enviando um arquivo.")

colA, colB = st.columns([1, 2])
with colA:
    enviar = st.button("🚀 Enviar para API", type="primary")
with colB:
    mostrar_req = st.checkbox("Mostrar payload enviado", value=False)

# =========================
# Envio
# =========================
if enviar:
    try:
        payload = _carregar_payload()
        url = f"{api_base}{endpoint}"
        if pretty:
            url += "?pretty=true"

        t0 = time.time()
        resp = requests.post(url, json=payload, timeout=60)
        dt = (time.time() - t0) * 1000

        st.success(f"Status {resp.status_code} • {dt:.0f} ms • Endpoint: {url}")

        if mostrar_req:
            st.subheader("Request body")
            st.code(json.dumps(payload, ensure_ascii=False, indent=2), language="json")

        # Resposta texto (PlainText)
        if resp.headers.get("content-type", "").startswith("text/plain"):
            st.subheader("Resposta (texto formatado)")
            st.code(resp.text, language="json")
        else:
            # Resposta JSON
            data = resp.json()
            st.subheader("Resposta (JSON)")
            st.json(data)

            # Se for único processo, exibir destaque de decisão
            if isinstance(data, dict):
                st.markdown("### Resumo")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Resultado", str(data.get("resultado", "?")))
                with c2:
                    st.write("**Citações:**", data.get("citacoes", []))
                st.write("**Justificativa:**")
                st.write(data.get("justificativa", ""))

            # Se for lista, mostrar cards simples
            if isinstance(data, list):
                st.markdown("### Resumo (lista)")
                for i, item in enumerate(data, start=1):
                    with st.expander(f"Processo {i} • {item.get('numeroProcesso', '')}"):
                        st.write(f"**Resultado:** {item.get('resultado')}")
                        st.write(f"**Citações:** {item.get('citacoes')}")
                        st.write("**Justificativa:**")
                        st.write(item.get("justificativa", ""))
                        st.code(json.dumps(item, ensure_ascii=False, indent=2), language="json")

    except json.JSONDecodeError as e:
        st.error(f"JSON inválido: {e}")
    except requests.RequestException as e:
        st.error(f"Erro ao chamar API: {e}")
    except Exception as e:
        st.error(f"Erro: {e}")
