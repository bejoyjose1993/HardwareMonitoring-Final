# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies (disable virtualenv for simplicity)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
RUN poetry run pytest -v --disable-warnings

# Set PYTHONPATH
ENV PYTHONPATH=/app/src

# Default environment variables
ENV TRANSPORT=http
ENV ENDPOINT=http://0.0.0.0:8000/ingest
ENV BROKER=mosquitto
ENV PORT=1883
ENV INTERVAL=5

# Expose FastAPI port
EXPOSE 8000

# Run the unified EdgeMonitor + API server
CMD ["poetry", "run", "python", "src/run_all.py"]
