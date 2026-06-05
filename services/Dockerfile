FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY pipeline.cron /app/pipeline.cron
RUN pip install --no-cache-dir -r /app/requirements.txt
