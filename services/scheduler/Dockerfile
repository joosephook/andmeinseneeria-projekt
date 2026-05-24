FROM python:3.11-slim
WORKDIR /app

# Install cron and dependencies
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy scripts and requirements
COPY scripts/ /app/scripts/
COPY ingest_stub/ /app/ingest/
COPY transform_stub/ /app/transform/
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Add crontab
COPY pipeline.cron /etc/cron.d/pipeline-cron
RUN chmod 0644 /etc/cron.d/pipeline-cron && crontab /etc/cron.d/pipeline-cron

RUN mkdir -p /var/log/pipeline

CMD ["/usr/sbin/cron", "-f"]
