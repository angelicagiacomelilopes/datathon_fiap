FROM python:3.9-slim

WORKDIR /app

# Instalar dependências
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY app/ ./app/

# Variável de ambiente para incluir o diretório atual no PYTHONPATH
ENV PYTHONPATH=/app

# Expor porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
