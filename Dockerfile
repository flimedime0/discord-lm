# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# App code
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
RUN pip install --no-cache-dir -e .

# Entrypoint (env vars come from docker-compose)
CMD ["python", "-m", "discord_lm_bot.discord_bot"]
