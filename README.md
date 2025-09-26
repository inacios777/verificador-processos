⚖️ Verificador de Processos Judiciais com LLM

📜 Visão Geral

Esta aplicação automatiza a análise de processos judiciais avaliando se créditos devem ser aprovados, rejeitados ou marcados como incompletos, de acordo com uma política de regras internas.
A decisão é feita com suporte de um LLM (Large Language Model), garantindo explicabilidade e padronização.

O projeto inclui:

Módulo de verificação com regras (POL-1 a POL-8).

API FastAPI para análise de processos e monitoramento.

Interface em Streamlit para interação manual.

Integração com n8n para orquestração de fluxo.

Deploy containerizado com Docker.

--------------------------------------------------------------
🎯 Objetivo

Receber dados de um processo judicial no schema definido.
Aplicar automaticamente as regras da Política usando um LLM.

Retornar JSON estruturado com decisão:

"approved"

"rejected"

"incomplete"

Incluir justificativa textual e citações das regras aplicadas.

----------------------------------------------------------------
🧩 Estrutura do Projeto

🔹 Backend (API)

FastAPI (app/main.py)

Endpoints principais:

POST /analisar → retorna saída em texto formatado.

POST /analisar_json → retorna saída em JSON estruturado.

GET /health → status de saúde.

🔹 Módulos Core

modelos.py → Define estruturas Pydantic (Base, Mínima, Resposta).

politica.py → Regras POL-1 a POL-8.

preprocessador.py → Converte ProcessoBase → ProcessoMinimo.

llm.py → Monta prompt, envia ao LLM e valida resposta.

decisao.py → Orquestra análise, formata resposta e envia webhook ao n8n.

formatador.py → Padroniza saída legível (JSON-like).

🔹 Interface Visual

Streamlit UI (ui/streamlit_app.py)

Permite enviar processos via textarea ou upload de arquivo.

Visualização de decisão em texto ou JSON, com destaques de justificativa e citações.

🔹 Testes

tests/teste_decisao.py → Envia exemplos de processos para API local.

----------------------------------------------------------------
⚙️ Como Rodar Localmente

1. Clonar o Repositório

git clone https://github.com/seu-usuario/verificador-processos.git

cd verificador-processos

2. Configurar Variáveis de Ambiente

Crie um arquivo .env com:

OPENAI_API_KEY=your_openai_api_key

OPENAI_MODEL=gpt-4o

N8N_WEBHOOK_URL=https://seu-n8n.com/webhook/verificador

API_URL=http://127.0.0.1:8000

3. Rodar com Docker Compose

docker-compose up --build

API disponível em → http://127.0.0.1:8000

Streamlit disponível em → http://127.0.0.1:8501

----------------------------------------------------------------
🔗 Endpoints da API

GET /health → Checagem de saúde.
POST /analisar → Recebe dict ou list de dicts e retorna texto formatado.
POST /analisar_json → Recebe dict ou list de dicts e retorna JSON estruturado.
📌 A documentação automática do FastAPI (Swagger/OpenAPI) está disponível em:
http://127.0.0.1:8000/docs

----------------------------------------------------------------
🖥️ Interface Visual (Streamlit)

Acesse via navegador em http://127.0.0.1:8501.

Recursos:

Input por textarea ou upload de arquivo JSON.

Escolha entre saída Texto ou JSON.

Destaque de decisão, justificativa e citações.

📂 Formato do JSON

Único processo: objeto { ... } contendo os campos principais do processo.

Múltiplos processos: lista [ { ... }, { ... }, ... ] com cada processo no mesmo formato.

----------------------------------------------------------------
📜 Política Implementada

POL-1: Somente processos transitados em julgado e em fase de execução.

POL-2: Valor da condenação é obrigatório.

POL-3: Não comprar valores < R$1.000,00.

POL-4: Não comprar processos trabalhistas.

POL-5: Não comprar se autor faleceu sem habilitação de herdeiros.

POL-6: Não comprar com substabelecimento sem reserva de poderes.

POL-7: Honorários (contratuais, periciais, sucumbenciais) devem ser informados quando existirem.

POL-8: Se faltar documento essencial, marcar como "incomplete".

----------------------------------------------------------------
✅ Critérios de Avaliação atendidos

✔️ Uso obrigatório do LLM (OpenAI API).

✔️ API REST com FastAPI + documentação automática.

✔️ UI interativa em Streamlit.

✔️ Saída controlada e explicável (resultado, justificativa, citacoes).

✔️ Deploy containerizado via Docker/Docker Compose.

✔️ Integração com n8n para orquestração de fluxo.

    Assunto: Decisão do Processo 1000001-11.2023.4.01.0001

        Decisão do Processo 1000001-11.2023.4.01.0001

        -> Resultado: incomplete

        -> Justificativa: Faltam documentos essenciais: certidão de trânsito em julgado e cumprimento definitivo iniciado.
        
        -> Citações: POL-1, POL-2, POL-8

✔️ Testes básicos via tests/teste_decisao.py.

----------------------------------------------------------------
🚀 Deploy

O sistema pode ser facilmente publicado em Railway, Render, Fly.io ou similares, expondo:

Porta 8000 (API).

Porta 8501 (Streamlit UI).
