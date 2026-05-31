-- Minimal schema init for the pipeline (staging, quality, mart, logs)
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
    contract_number TEXT NOT NULL,
    debt_amount NUMERIC(18,2) NOT NULL,
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
    debt_days INTEGER,
    UNIQUE (contract_key, snapshot_date),
    CHECK (debt_days IS NULL OR debt_days >= 0)
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

CREATE OR REPLACE VIEW mart.v_overdues_summary AS
SELECT
fd.snapshot_date,
SUM(fd.debt_amount) AS company_debtsum_total,
ROUND(
SUM(fd.debt_amount * fd.debt_days) / NULLIF(SUM(fd.debt_amount), 0)
) AS weighted_avg_debtdays,
COUNT(DISTINCT fd.company_key) AS company_count,
COUNT(DISTINCT (fd.company_key, fd.contract_key)) AS contract_count
FROM mart.fact_debt_snapshot fd
WHERE fd.debt_days IS NOT NULL
GROUP BY
snapshot_date;
