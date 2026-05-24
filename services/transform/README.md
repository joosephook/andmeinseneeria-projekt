# Transform service

Simple transform that reads `staging.ingested_files` and `staging.raw_debt_rows`, upserts dimensions (`mart.dim_company`, `mart.dim_contract`, `mart.dim_date`, `mart.dim_file`), writes/updates `mart.fact_debt_snapshot` and computes `mart.kpi_daily_debt`.

Configure PostgreSQL connection via environment variables: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.

Run locally:

```bash
python transform.py
```
