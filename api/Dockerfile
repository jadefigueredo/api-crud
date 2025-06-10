FROM python:3.9-slim

WORKDIR /app

# Variáveis de ambiente

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Cria um usuário não-root para executar a aplicação
RUN adduser --disabled-password --gecos '' appuse
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Define verificação de saúde
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando para executar a aplicação
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
CMD ["FLASK_APP=app.py", "flask", "run", "--host=0.0.0.0", "--port=5000"]
