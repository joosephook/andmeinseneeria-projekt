FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ingest_xlsx.py ./
COPY README.md ./
CMD ["python", "ingest_xlsx.py"]
