import json

TOP_LEVEL_ORDER = [
    "numeroProcesso", "classe", "orgaoJulgador", "ultimaDistribuicao",
    "valorCausa", "assunto", "segredoJustica", "justicaGratuita",
    "siglaTribunal", "esfera", "valorCondenacao",
    "documentos",
    "honorarios", "resultado", "justificativa", "citacoes",
]

DOCS_ORDER = [
    "sentencaMerito",
    "transitoJulgado",
    "cumprimentoDefinitivoIniciado",
    "calculosApresentados",
    "intimacaoEntePublico",
    "prazoImpugnacaoAberto",
    "requisitorio",
    "cessaoPreviaPagamento",
    "substabelecimentoSemReserva",
    "obitoAutor",
]

def _dump_inline(value):
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(", ", ": "))
    return json.dumps(value, ensure_ascii=False, indent=2)

def formatar_resultado(resultado: dict) -> str:
    """
    Formata UM resultado de processo no estilo do teste_decisao.py
    """
    if "documentos" not in resultado:
        resultado["documentos"] = {}

    keys = list(resultado.keys())
    ordered_top = [k for k in TOP_LEVEL_ORDER if k in keys]
    leftovers = sorted([k for k in keys if k not in TOP_LEVEL_ORDER])
    final_top = ordered_top + leftovers

    idx_docs = final_top.index("documentos")
    before = final_top[:idx_docs]
    after  = final_top[idx_docs+1:]

    linhas = ["{"]

    # BEFORE
    for k in before:
        val = _dump_inline(resultado[k]) if k == "citacoes" else json.dumps(resultado[k], ensure_ascii=False, indent=2)
        linhas.append(f'  "{k}": {val},')

    # DOCUMENTOS
    linhas.append('  "documentos": {')
    documentos = resultado.get("documentos", {}) or {}
    ordered_docs = [d for d in DOCS_ORDER if d in documentos]
    leftover_docs = sorted([d for d in documentos.keys() if d not in DOCS_ORDER])
    final_docs = ordered_docs + leftover_docs

    for i, doc in enumerate(final_docs, start=1):
        val_inline = json.dumps(documentos[doc], ensure_ascii=False, separators=(", ", ": "))
        comma = "," if i < len(final_docs) else ""
        linhas.append(f'    "{doc}": {val_inline}{comma}')
    linhas.append("  }" + ("," if after else ""))

    # AFTER
    for i, k in enumerate(after, start=1):
        is_last = i == len(after)

        if k == "honorarios":
            h = resultado.get("honorarios") or {}
            linhas.append('  "honorarios": {')
            itens = list(h.items())
            for j, (hk, hv) in enumerate(itens, start=1):
                comma2 = "," if j < len(itens) else ""
                linhas.append(f'    "{hk}": {json.dumps(hv, ensure_ascii=False)}{comma2}')
            linhas.append("  }" + ("," if not is_last else ""))
            continue

        if k == "citacoes":
            val = json.dumps(resultado[k], ensure_ascii=False, separators=(", ", ": "))
        else:
            val = json.dumps(resultado[k], ensure_ascii=False, indent=2)

        line = f'  "{k}": {val}'
        linhas.append(line + ("," if not is_last else ""))

    linhas.append("}")
    return "\n".join(linhas)

def formatar_resultados(resultados: list) -> str:
    """
    Formata LISTA de resultados, estilo === Teste 1 ===
    """
    blocos = []
    for i, r in enumerate(resultados, start=1):
        blocos.append(f"=== Teste {i} ===\n{formatar_resultado(r)}")
    return "\n\n".join(blocos)
