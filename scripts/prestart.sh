#!/usr/bin/env bash
set -euo pipefail

# Pre-start wrapper: kontrollib hosti porte ja käivitab docker-compose kui vabad
# Usage: ./scripts/prestart.sh [-f docker-compose.example.yml]

COMPOSE_FILE=docker-compose.example.yml

while getopts ":f:" opt; do
  case ${opt} in
    f ) COMPOSE_FILE=$OPTARG ;;
    \? ) echo "Usage: $0 [-f compose-file]"; exit 2 ;;
  esac
done

echo "Pre-start: parsing compose file: ${COMPOSE_FILE}"

if command -v python >/dev/null 2>&1; then
  python scripts/check_free_ports.py --compose-file "${COMPOSE_FILE}"
  rc=$?
else
  echo "Python not found in PATH. Please install Python or run check_free_ports.py manually." >&2
  exit 2
fi

if [ "$rc" -ne 0 ]; then
  echo "Port conflict detected. Aborting docker compose up." >&2
  exit $rc
fi

echo "Ports available. Starting docker compose..."
docker compose -f "${COMPOSE_FILE}" up --build -d
echo "Docker compose started. Use 'docker compose ps' to check services."
