⚖️ Verificador de Processos Judiciais

Este projeto implementa um sistema automatizado para analisar processos judiciais e decidir se o crédito pode ser aprovado, rejeitado ou considerado incompleto.
As decisões seguem regras internas (POL-1 até POL-8) aplicadas com auxílio de Inteligência Artificial (LLM).

🚀 Como rodar com Docker

1. Build da imagem
docker build -t verificador-processos .

2. Rodar o container
docker run -p 8000:8000 -p 8501:8501 verificador-processos

📖 Como acessar

API (FastAPI + Swagger):
http://localhost:8000/docs

Interface Web (Streamlit):
http://localhost:8501

🔗 Endpoints principais

POST /analisar → retorna decisão em texto formatado
POST /analisar_json → retorna decisão em JSON estruturado
GET /health → confirma se a API está online

🖥️ Interface Gráfica (UI com Streamlit)

Além da API, o sistema conta com uma interface web amigável feita em Streamlit, 
onde o usuário pode testar processos sem precisar usar Swagger ou terminal.

Na UI, é possível:
Colar um JSON diretamente em um campo de texto;
Fazer upload de um arquivo .json com um ou mais processos;
Escolher se a saída será texto formatado ou JSON estruturado;
Visualizar de forma clara o resultado, justificativa e citações de cada processo.

Acesso local:
http://localhost:8501

🌐 Integração com n8n

Este sistema envia os resultados para um workflow no n8n, que permite:
Receber os dados via Webhook;
Registrar a decisão automaticamente;
Enviar notificação por email exemplo:

Decisão do Processo 1000011-11.2016.4.10.0011

-> Resultado: approved
-> Justificativa: O processo atende a todas as regras de aprovação mínima e não há regras de rejeição aplicáveis.
-> Citações: POL-1, POL-2, POL-7

Webhook público configurado:
https://rafaaiva.app.n8n.cloud/webhook/18048e37-cf83-4d6a-814f-5ab281ddd672

📖 Exemplos de Entrada e Saída

Entrada

{
  "numeroProcesso": "1000001-11.2023.4.01.0001",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "10ª VARA FEDERAL - DF",
  "ultimaDistribuicao": "2024-07-01T10:00:00Z",
  "assunto": "Previdenciário",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF1",
  "esfera": "Federal",
  "valorCondenacao": 15000,
  "documentos": [
    {
      "id": "DOC-1-1",
      "dataHoraJuntada": "2023-07-10T08:00:00",
      "nome": "Sentença de Mérito",
      "texto": "SENTENÇA..."
    }
  ],
  "movimentos": [],
  "honorarios": {}
}

Saída

{
  "numeroProcesso": "1000001-11.2023.4.01.0001",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "10ª VARA FEDERAL - DF",
  "ultimaDistribuicao": "2024-07-01T10:00:00Z",
  "valorCausa": null,
  "assunto": "Previdenciário",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF1",
  "esfera": "Federal",
  "valorCondenacao": 15000,
  "documentos": {
    "sentencaMerito": {"data": "2023-07-10T08:00:00","resumo": "SENTENÇA..."},
    "transitoJulgado": {"status": "Não","indicacao": null },
    "cumprimentoDefinitivoIniciado": {"status": "Não","data": null },
    "calculosApresentados": {"status": "Não","data": null },
    "intimacaoEntePublico": {"status": "Não","data": null },
    "prazoImpugnacaoAberto": {"status": "Não","data": null },
    "requisitorio": {"tipo": null,"valor": null,"data_expedicao": null },
    "cessaoPreviaPagamento": {"status": "Não","detalhes": ""},
    "substabelecimentoSemReserva": {"status": "Não"},
    "obitoAutor": {"status": "Não"}
  },
  "honorarios": {},
  "resultado": "approved",
  "justificativa": "Processo transitado em julgado e em execução",
  "citacoes": ["POL-1", "POL-2"]
}


📌 Estrutura do projeto

app/

 ├── __init__.py      # marcador técnico

 ├── decisao.py        # Fluxo central de análise

 ├── formatador.py     # Saída formatada (texto/JSON)

 ├── llm.py            # Conexão com LLM (OpenAI GPT)

 ├── main.py           # API (FastAPI)

 ├── modelos.py        # Estruturas de dados (entrada, mínima, saída)

 ├── politica.py       # Regras de decisão (POL-1 até POL-8)

 └── preprocessador.py # Normalização dos dados brutos

tests/

 ├── teste_decisao.py  # Script de testes

 ├── teste_unico.json  # Exemplo de um processo

 └── teste_lista_11.json # Exemplo de múltiplos processos

ui/

 └── streamlit_app.py  # Interface gráfica

.env                   # Dados sensíveis ou configuráveis

docker-compose.yml     # Orquestração local

Dockerfile             # Configuração para rodar em container

README.md              # Este arquivo

requirements.txt       # Dependências Python
