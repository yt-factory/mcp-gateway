FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --no-dev --frozen

COPY src/ ./src/

RUN mkdir -p /app/credentials /app/.cache

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "-m", "src.server"]
