#!/bin/sh
set -e
LOGDIR=/var/log/pipeline
mkdir -p "$LOGDIR"
echo "Starting pipeline run: $(date -u)" >> "$LOGDIR/run.log"

echo "Running ingest..." >> "$LOGDIR/run.log"
python /app/ingest/ingest_xlsx.py >> "$LOGDIR/run.log" 2>&1 || { echo "ingest failed" >> "$LOGDIR/run.log"; exit 1; }

echo "Running transform..." >> "$LOGDIR/run.log"
python /app/transform/transform.py >> "$LOGDIR/run.log" 2>&1 || { echo "transform failed" >> "$LOGDIR/run.log"; exit 1; }

echo "Pipeline finished: $(date -u)" >> "$LOGDIR/run.log"
