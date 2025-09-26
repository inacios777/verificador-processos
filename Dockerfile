# 📌 Função deste arquivo:
# Construir a imagem Docker que executa simultaneamente a API FastAPI e a interface Streamlit,
# empacotando toda a aplicação em um ambiente isolado e portátil.
#
# -------------------------------------------------
# Principais responsabilidades:
# -------------------------------------------------
# Imagem base:
#   ➡ Usa python:3.11-slim para reduzir o tamanho final do container.
#
# Diretório de trabalho:
#   ➡ Define /app como diretório principal dentro do container.
#
# Cópia do projeto:
#   ➡ Copia todos os arquivos locais para /app.
#
# Instalação de dependências:
#   ➡ Atualiza o pip.
#   ➡ Instala as dependências listadas em requirements.txt.
#
# Exposição de portas:
#   - 8000 → API FastAPI
#   - 8501 → Interface Streamlit
#
# Comando de execução:
#   ➡ Executa em paralelo:
#      - uvicorn app.main:app → inicia a API na porta 8000
#      - streamlit run ui/streamlit_app.py → inicia a interface Streamlit na porta 8501


# -------------------------------
# Imagem base com Python
# -------------------------------
FROM python:3.11-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto para dentro do container
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expor portas:
# 8000 -> FastAPI
# 8501 -> Streamlit
EXPOSE 8000 8501

# -------------------------------
# Comando de execução
# -------------------------------
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run ui/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
