# Relatsiooniline PostgreSQL Andmemudel

## Eesmärk

Dokumendi eesmärk on kirjeldada PostgreSQL skeemid, tabelid, seosed, indeksid ja constraintid, mille abil SAP võlaandmed laaditakse, kontrollitakse ja teisendatakse analüütiliseks kihiks.

## Ulatus

Ulatus hõlmab skeeme `staging`, `quality`, `mart` ja `logs` ning põhitabeleid toorandmete, kvaliteeditulemuste, pipeline logide ja dashboardi mart kihi jaoks.

## Põhikirjeldus

Andmemudel jaguneb neljaks kihiks. `staging` hoiab failide metaandmeid ja toorread. `quality` hoiab valideerimistulemusi. `logs` hoiab töövoo käivituste infot. `mart` hoiab dashboardi ja tulevase ML komponendi jaoks sobivaid dimensioone ja faktitabeleid.

## Skeemid Ja Tabelid

| Skeem | Tabel | Roll |
|---|---|---|
| `staging` | `raw_debt_rows` | SAP failist loetud toorread. |
| `staging` | `ingested_files` | Failide metaandmed ja duplikaadikontroll. |
| `quality` | `quality_results` | Rea- ja failipõhised kvaliteeditulemused. |
| `logs` | `pipeline_runs` | Pipeline käivituste logi. |
| `mart` | `dim_company` | Ettevõtte dimensioon. |
| `mart` | `dim_contract` | Lepingu dimensioon. |
| `mart` | `dim_date` | Kuupäeva dimensioon. |
| `mart` | `dim_file` | Faili dimensioon. |
| `mart` | `fact_debt_snapshot` | Päevane lepingu võlasnapshot. |
| `mart` | `kpi_daily_debt` | Päevased dashboardi KPI-d. |

## DDL Näited

```sql
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS quality;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS logs;

CREATE TABLE IF NOT EXISTS staging.ingested_files (
    file_id BIGSERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_checksum TEXT NOT NULL UNIQUE,
    source_path TEXT NOT NULL,
    report_date DATE,
    ingested_at TIMESTAMPTZ DEFAULT now(),
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS staging.raw_debt_rows (
    raw_row_id BIGSERIAL PRIMARY KEY,
    file_id BIGINT REFERENCES staging.ingested_files(file_id),
    row_number INTEGER NOT NULL,
    registry_code TEXT,
    contract_number TEXT,
    debt_amount NUMERIC(18,2),
    debt_days INTEGER,
    raw_payload JSONB,
    loaded_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS quality.quality_results (
    quality_result_id BIGSERIAL PRIMARY KEY,
    file_id BIGINT REFERENCES staging.ingested_files(file_id),
    raw_row_id BIGINT REFERENCES staging.raw_debt_rows(raw_row_id),
    rule_code TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    checked_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS logs.pipeline_runs (
    pipeline_run_id BIGSERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL,
    file_id BIGINT,
    step_name TEXT,
    message TEXT
);

CREATE TABLE IF NOT EXISTS mart.dim_company (
    company_key BIGSERIAL PRIMARY KEY,
    registry_code TEXT NOT NULL UNIQUE,
    company_name TEXT
);

CREATE TABLE IF NOT EXISTS mart.dim_contract (
    contract_key BIGSERIAL PRIMARY KEY,
    contract_number TEXT NOT NULL,
    company_key BIGINT NOT NULL REFERENCES mart.dim_company(company_key),
    UNIQUE (contract_number, company_key)
);

CREATE TABLE IF NOT EXISTS mart.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS mart.dim_file (
    file_key BIGSERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_checksum TEXT NOT NULL UNIQUE,
    ingested_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS mart.fact_debt_snapshot (
    debt_snapshot_key BIGSERIAL PRIMARY KEY,
    company_key BIGINT NOT NULL REFERENCES mart.dim_company(company_key),
    contract_key BIGINT NOT NULL REFERENCES mart.dim_contract(contract_key),
    date_key INTEGER NOT NULL REFERENCES mart.dim_date(date_key),
    file_key BIGINT NOT NULL REFERENCES mart.dim_file(file_key),
    snapshot_date DATE NOT NULL,
    debt_amount NUMERIC(18,2) NOT NULL,
    debt_days INTEGER NOT NULL,
    UNIQUE (contract_key, snapshot_date)
);

CREATE TABLE IF NOT EXISTS mart.kpi_daily_debt (
    snapshot_date DATE PRIMARY KEY,
    total_debt_amount NUMERIC(18,2),
    weighted_avg_debt_days NUMERIC(18,4),
    max_debt_days INTEGER,
    debt_contract_count INTEGER,
    debt_company_count INTEGER,
    calculated_at TIMESTAMPTZ DEFAULT now()
);
```

## Indeksid Ja Constraintid

| Objekt | Soovitus | Põhjus |
|---|---|---|
| `staging.ingested_files.file_checksum` | `UNIQUE` | Takistab sama faili korduslaadimist. |
| `staging.raw_debt_rows(file_id, row_number)` | `UNIQUE` | Tagab rea kordumatuse faili sees. |
| `mart.fact_debt_snapshot(contract_key, snapshot_date)` | `UNIQUE` | Üks rida ühe lepingu ühe raportikuupäeva kohta. |
| `mart.fact_debt_snapshot(snapshot_date)` | indeks | Kiirendab dashboardi ajafiltreid. |
| `mart.dim_company.registry_code` | `UNIQUE` ja indeks | Kiirendab ettevõtte järgi filtreerimist. |
| `debt_amount` | `CHECK (debt_amount >= 0)` mart kihis | Mart kihis ei tohiks olla negatiivseid võlasummasid. |
| `debt_days` | `CHECK (debt_days >= 0)` mart kihis | Võlapäevad ei tohiks olla negatiivsed. |

## Tehnilised Märkused

Staging kihis võib lubada rohkem puudulikke väärtusi, sest kvaliteedikontroll peab suutma vigased read salvestada ja raporteerida. Mart kihis tuleb kasutada rangemaid constraint'e, sest see kiht teenindab dashboardi ja analüütilisi päringuid.

## Küsimused

1. Kas ühe lepingu kohta võib samal päeval olla mitu rida? Jah.
2. Kui kaua tuleb toorfaile ja laadimisajalugu säilitada? Staging 7 päeva.
3. Kas ettevõtte nimi tuleb allikast või välisest registrist? Peame tegema aruande muudetud registrikoodide kaupa - paraku originaalandmed on konfidentsiaalsed. Ettevõtte nimi on kustutatud, jäetud muudetud registrikood.
