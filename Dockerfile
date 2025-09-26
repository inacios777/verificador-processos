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