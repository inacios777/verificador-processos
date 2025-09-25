from .modelos import ProcessoBase, ProcessoMinimo


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def converter_para_minimo(processo: ProcessoBase) -> ProcessoMinimo:
    """
    📌 Converte a estrutura base (ProcessoBase) em uma estrutura mínima (ProcessoMinimo),
    já normalizando documentos e movimentos em camelCase para atender o schema exigido.
    """

    documentos_snake = {
      "sentenca_merito": {
        "data": next((d.data_hora_juntada for d in processo.documentos if "sentença" in d.nome.lower()), None),
        "resumo": next((d.texto[:50] for d in processo.documentos if "sentença" in d.nome.lower()), None),
      },
      "transito_julgado": {
        "status": "Sim" if any("trânsito" in d.nome.lower() for d in processo.documentos) else "Não",
        "indicacao": next((d.nome for d in processo.documentos if "trânsito" in d.nome.lower()), None),
      },
      "cumprimento_definitivo_iniciado": {
        "status": "Sim" if any("cumprimento definitivo" in m.descricao.lower() for m in processo.movimentos) else "Não",
        "data": next((m.data_hora for m in processo.movimentos if "cumprimento definitivo" in m.descricao.lower()),
                     None),
      },
      "calculos_apresentados": {
        "status": "Sim" if any("cálculo" in d.nome.lower() for d in processo.documentos) else "Não",
        "data": next((d.data_hora_juntada for d in processo.documentos if "cálculo" in d.nome.lower()), None),
      },
      "intimacao_ente_publico": {
        "status": "Sim" if any("intimação" in m.descricao.lower() for m in processo.movimentos) else "Não",
        "data": next((m.data_hora for m in processo.movimentos if "intimação" in m.descricao.lower()), None),
      },
      "prazo_impugnacao_aberto": {
        "status": "Sim" if any("impugnação" in m.descricao.lower() for m in processo.movimentos) else "Não",
        "data": next((m.data_hora for m in processo.movimentos if "impugnação" in m.descricao.lower()), None),
      },
      "requisitorio": {
        "tipo": "RPV" if any("rpv" in d.nome.lower() for d in processo.documentos) else None,
        "valor": next((getattr(d, "valor", None) for d in processo.documentos if "rpv" in d.nome.lower()), None),
        "data_expedicao": next((d.data_hora_juntada for d in processo.documentos if "rpv" in d.nome.lower()), None),
      },
      "cessao_previa_pagamento": {
        "status": "Sim" if any("cessão" in d.nome.lower() for d in processo.documentos) else "Não",
        "detalhes": next((d.texto[:50] for d in processo.documentos if "cessão" in d.nome.lower()), ""),
      },
      "substabelecimento_sem_reserva": {
        "status": "Sim" if any("substabelecimento" in d.nome.lower() and "sem reserva" in d.nome.lower() for d in
                               processo.documentos) else "Não"
      },
      "obito_autor": {
        "status": "Sim" if any("óbito" in d.nome.lower() for d in processo.documentos) else "Não"
      },
    }

    # Converter chaves snake_case → camelCase
    documentos_camel = {snake_to_camel(k): v for k, v in documentos_snake.items()}

    return ProcessoMinimo(
        numero_processo=processo.numero_processo,
        classe=processo.classe,
        orgao_julgador=processo.orgao_julgador,
        ultima_distribuicao=processo.ultima_distribuicao,
        assunto=processo.assunto,
        valor_causa=processo.valor_causa,
        valor_condenacao=processo.valor_condenacao,
        segredo_justica=processo.segredo_justica,
        justica_gratuita=processo.justica_gratuita,
        sigla_tribunal=processo.sigla_tribunal,
        esfera=processo.esfera,
        documentos=documentos_camel,
        honorarios = processo.honorarios if processo.honorarios else None
    )
