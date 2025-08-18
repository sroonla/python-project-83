FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY . .

RUN uv pip install --system -e .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "page_analyzer.app:app"]