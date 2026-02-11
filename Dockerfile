# Imagem base estável
FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Diretório de trabalho
WORKDIR /app

ENV PYTHONPATH=/app
# Instala uv
RUN pip install --no-cache-dir uv

# Copia apenas arquivos de dependência primeiro (melhora cache)
COPY pyproject.toml uv.lock ./

# Cria ambiente virtual dentro do projeto
RUN uv venv

# Instala dependências exatamente como no lock
RUN uv sync --frozen --no-dev

# Copia restante da aplicação
COPY . .

# Expõe porta do Streamlit
EXPOSE 8501

# Executa usando caminho absoluto (evita problema de PATH)
CMD ["/app/.venv/bin/streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
