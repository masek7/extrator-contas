FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app


RUN pip install uv


COPY pyproject.toml uv.lock ./


RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
