"""

📌 Função deste arquivo:

Definir todas as regras de política (POL-1 até POL-8) que orientam a decisão de compra dos créditos processuais.
Essas regras servem como critérios de elegibilidade, restrição e completude de dados,
sendo usadas pelo verificador e pelo LLM.

------------------------------------------------------------------------------------------------------------------------
Três grupos de políticas:

Elegibilidade:
➡ (POL-1) Apenas processos transitados em julgado e em fase de execução são aceitos.
➡ (POL-2) O valor da condenação deve estar obrigatoriamente informado.

Restrições:
➡ (POL-3) Condenações com valor menor que R$1.000,00 não são aceitas.
➡ (POL-4) Processos da esfera trabalhista são rejeitados.
➡ (POL-5) Em caso de óbito do autor sem habilitação de herdeiros, o processo é recusado.
➡ (POL-6) Substabelecimento sem reserva de poderes inviabiliza a compra.

Completude de dados:
➡ (POL-7) É obrigatório informar honorários contratuais, periciais e sucumbenciais quando existirem.
➡ (POL-8) Se faltar documento essencial (certidão de trânsito em julgado, valor da condenação, cumprimento definitivo iniciado), o processo deve ser marcado como incomplete.

"""

POLITICA = {
  # -------------------------------------------------------------------------------------------------------------------
    # Grupo: Elegibilidade
  # -------------------------------------------------------------------------------------------------------------------
    "POL-1": (
        "Apenas compramos créditos de processos transitados em julgado e em fase de execução. "
        "Exemplo: um processo com certidão de trânsito em julgado e movimento de 'cumprimento definitivo iniciado'."
    ),
    "POL-2": (
        "É obrigatório informar o valor da condenação (campo valorCondenacao). "
        "Exemplo: valorCondenacao = 67.592,00."
    ),

  # -------------------------------------------------------------------------------------------------------------------
    # Grupo: Restrições
  # -------------------------------------------------------------------------------------------------------------------
    "POL-3": (
        "Se o valor da condenação for menor que R$ 1.000,00, não compramos. "
        "Exemplo: valorCondenacao = 500,00."
    ),
    "POL-4": (
        "Condenações na esfera trabalhista não são aceitas. "
        "Exemplo: esfera = 'Trabalhista'."
    ),
    "POL-5": (
        "Se houver óbito do autor sem habilitação no inventário, não compramos. "
        "Exemplo: documento indica óbito do autor, mas não há habilitação de herdeiros."
    ),
    "POL-6": (
        "Se houver substabelecimento sem reserva de poderes, não compramos. "
        "Exemplo: documento intitulado 'Substabelecimento sem reserva de poderes'."
    ),

  # ------------------------------------------------------------------------------------------------------------------
    # Grupo: Completude de dados
  # ------------------------------------------------------------------------------------------------------------------
    "POL-7": (
        "É obrigatório informar honorários contratuais, periciais e sucumbenciais quando existirem. "
        "Exemplo: sentença fixou honorários sucumbenciais, periciais, sucumbenciais. "
    ),
    "POL-8": (
      "Se faltar qualquer documento essencial, o processo deve ser marcado como 'incomplete'. "
      "Essenciais incluem: certidão de trânsito em julgado, valor da condenação e cumprimento definitivo iniciado. "
      "Exemplo: processo sem certidão de trânsito em julgado, sem valor da condenação informado ou sem cumprimento definitivo iniciado."
    )
}

# Texto concatenado para envio ao LLM
POLITICA_TEXTO = "\n".join([f"{k}: {v}" for k, v in POLITICA.items()])
