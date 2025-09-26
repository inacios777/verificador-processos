"""

📌 Função deste arquivo:

Integrar o sistema ao LLM da OpenAI, enviando os dados já normalizados (ProcessoMinimo)
junto com as regras da política e recebendo a decisão estruturada em formato JSON.

------------------------------------------------------------------------------------------------------------------------
Principais responsabilidades:

Configuração do modelo:
➡ O modelo a ser usado é definido via variável de ambiente (OPENAI_MODEL).
➡ A chave da API (OPENAI_API_KEY) também é carregada do .env via dotenv.

Mensagem de sistema (SYSTEM_MSG):
➡ Define o comportamento esperado do LLM: um verificador jurídico rigoroso, que aplica apenas as regras
fornecidas sem interpretações adicionais.

Montagem do prompt (montar_prompt):
➡ Estrutura o contexto enviado ao LLM contendo:
Instruções claras de prioridade das regras (rejeição absoluta → aprovação mínima → completude → honorários).
Texto integral da política (POLITICA_TEXTO).
Estrutura mínima do processo em JSON (ProcessoMinimo).
➡ Reforça que a saída deve ser exclusivamente JSON válido com os campos resultado, justificativa e citacoes.

Decisão com LLM (decidir_com_llm):
➡ Constrói o cliente da OpenAI, envia o prompt e recebe a resposta.
➡ Garante saída em JSON usando response_format={"type": "json_object"}.
➡ Valida a resposta contra o modelo RespostaDecisao para assegurar conformidade.
➡ Caso a saída não seja JSON válido, levanta exceção (ValueError).

"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

from .modelos import ProcessoMinimo, RespostaDecisao
from .politica import POLITICA_TEXTO

# Modelo padrão (pode ser trocado no .env)
MODEL = os.getenv("OPENAI_MODEL")

# Mensagem de sistema para instruir o LLM
SYSTEM_MSG = """
# Sua característica profissional

- Você é um verificador jurídico altamente criterioso e profissional.
- Sua função é aplicar exclusivamente as regras fornecidas da política,sem interpretações 
além do que está explicitamente descrito.
"""

def montar_prompt(proc: ProcessoMinimo) -> str:
    """
    Cria o prompt com:
    # - Regras de decisão
    # - Texto da política (IDs + descrições)
    # - Estrutura mínima do processo em JSON
    """


    return f"""

# Instruções

- Aplique exclusivamente as regras definidas na política.
- Respeite a seguinte ordem de prioridade:

  1. **Regras de rejeição absoluta** (POL-3, POL-4, POL-5, POL-6).  
     - Se alguma delas for satisfeita, o resultado deve ser **"rejected"**, mesmo que também faltem documentos.  
     - Nesses casos, não use POL-8 na citação.
     - "resultado": "rejected",

  2. **Regras de aprovação mínima** (POL-1 e POL-2).  
     - Considere como documentos essenciais: Transito Julgado e Cumprimento Definitivo Iniciado. (POL-1) e valor da condenação (POL-2). 
     - Se um deles faltar, o processo deve ser **"incomplete"** com as citações correspondentes acrescida do (POL-8).

  3. **Regras de documento essencial** (POL-8).  
     - Só aplique o POL-8 quando faltar documento essencial (Transito Julgado e Cumprimento Definitivo Iniciado. (POL-1) e valor da condenação (POL-2).).  
     - "resultado": "incomplete",
     
  4. **Regras de honorários obrigatórios** (POL-7).  
     - Use POL-7 quando existir informações de honorários  

# Resposta
 
- A resposta deve ser em **JSON válido**, contendo:
  - resultado: apenas um dos valores em inglês: "approved", "rejected" ou "incomplete"
  - justificativa: explicação clara e objetiva do motivo da decisão
  - citacoes: lista com todos os IDs aplicados (ex.: ["POL-1", "POL-2"])

# Política
(use sempre os IDs exatamente como definidos)

{POLITICA_TEXTO}

# Decisão
Analise o processo abaixo e devolva SOMENTE o JSON solicitado. Não inclua nenhum texto fora do JSON.

PROCESSO_MINIMO:
{proc.model_dump_json(indent=2, exclude_none=True)}
"""

def decidir_com_llm(proc: ProcessoMinimo) -> RespostaDecisao:
    """
    Envia o ProcessoMinimo para o LLM e retorna uma RespostaDecisao validada.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = montar_prompt(proc)

    resp = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},  # força saída em JSON
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )

    conteudo = resp.choices[0].message.content

    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError:
        raise ValueError(f"Resposta inválida do LLM: {conteudo}")

    return RespostaDecisao.model_validate(dados)
