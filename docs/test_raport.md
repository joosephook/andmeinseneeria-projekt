# Ühe testi läbijooksutamise juhend

**Eeldused**

1. Docker Desktop on käivitatud
2. Oled projekti juurkaustas
3. .env fail on olemas (cp .env.example .env)
4. aruanne/ kaust on olemas koos XLSX failidega


## Samm 1 — Käivita pipeline
´´´bash
docker compose up -d postgres
docker compose up pipeline


# Oodatav tulemus terminalis:

pipeline-1 | INFO: Starting pipeline run: ...
pipeline-1 | INFO: Ingesting
pipeline-1 | INFO: DB connection established
pipeline-1 | INFO: Truncating tables...
pipeline-1 | INFO: Ingesting path='/data/aruanne/...'
pipeline-1 | INFO: Inserted XXXX rows for file_id=1
pipeline-1 | INFO: Transforming
pipeline-1 | INFO: MART_SUM_POSITIVE PASSED: ...
pipeline-1 | INFO: MART_CONTRACT_COUNT PASSED: ...
pipeline-1 | INFO: MART_SNAPSHOT_EXISTS PASSED
pipeline-1 | INFO: Computing KPIs...
pipeline-1 | INFO: Pipeline run end: ...
pipeline-1 exited with code 0
Kui näed exited with code 0 — pipeline õnnestus.
Kui näed exited with code 1 — vaata logi vigade jaoks.

**Samm 2 — Kontrolli staging kvaliteedikontrolle**
´´´bash

docker compose exec postgres psql -U debtuser -d debtdb -c 'SELECT status, COUNT(*) FROM quality.quality_results GROUP BY status;'



# Oodatav tulemus:
 status | count
--------+--------
 PASSED | 111748
(1 row)

# Kui näed FAILED ridu, jooksuta see käsk vigade nägemiseks:
´´´bash

docker compose exec postgres psql -U debtuser -d debtdb -c 'SELECT rule_code, message FROM quality.quality_results WHERE status = '"'"'FAILED'"'"' LIMIT 20;'



**Samm 3 — Kontrolli mart kontrollide tulemusi**
´´´
bash

docker compose up pipeline 2>&1 | grep -E "MART|ERROR|Pipeline run end"


# Oodatav tulemus:
INFO: MART_SUM_POSITIVE PASSED: 2025-12-31 total=11512776.47
INFO: MART_CONTRACT_COUNT PASSED: 2025-12-31 count=433
INFO: MART_SNAPSHOT_EXISTS PASSED
INFO: Pipeline run end: ...
Kui näed MART_... FAILED või Mart validation failed, on mart kihis probleem ja KPI-d ei uuendatud.

**Samm 4 — Kontrolli KPI tulemusi**
´´´bash

docker compose exec postgres psql -U debtuser -d debtdb -c 'SELECT snapshot_date, total_debt_amount FROM mart.kpi_daily_debt ORDER BY snapshot_date;'


# Oodatav tulemus:
 snapshot_date | total_debt_amount
---------------+------------------
 2025-12-31    |      11512776.47
 2026-01-31    |      12055180.64
 2026-02-28    |      12135459.50
 2026-03-31    |      12616636.23
 2026-04-30    |      13269924.35
(5 rows)
Kui tabel on tühi, ei läbinud mart kontrollid või pipeline katkeb enne KPI arvutust.

