# Ingest service

Simple Python-based ingest that scans `ARUANNE_DIR` for files named `LN002 Laenude võlgnevus.xlsx`,
derives `report_date` from file `date modified` minus one day, and inserts rows into `staging.ingested_files`
and `staging.raw_debt_rows` in the PostgreSQL database.

Configure via environment variables (see `.env.example`):

- `ARUANNE_DIR` - base directory to scan (default `/data/aruanne`)
- `POSTGRES_*` - DB connection settings

Run locally (when containerized, mount host `TMP/aruanne` to the container path):

```bash
python ingest_xlsx.py
```
