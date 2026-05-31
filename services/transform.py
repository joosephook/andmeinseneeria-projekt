import psycopg2
import logging
from utils import attempt_db_connect
import traceback

LOGGER = logging.getLogger(__file__)

def ensure_dim_date(cur, report_date):
    date_key = int(report_date.strftime('%Y%m%d'))
    cur.execute("INSERT INTO mart.dim_date (date_key, full_date, year, month, day) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (date_key) DO NOTHING",
                (date_key, report_date, report_date.year, report_date.month, report_date.day))
    return date_key

def upsert_company(cur, registry_code):
    if registry_code is None:
        return None
    cur.execute("INSERT INTO mart.dim_company (registry_code, company_name) VALUES (%s, %s) ON CONFLICT (registry_code) DO NOTHING RETURNING company_key",
                (registry_code, None))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("SELECT company_key FROM mart.dim_company WHERE registry_code = %s", (registry_code,))
    return cur.fetchone()[0]

def upsert_contract(cur, contract_number, company_key):
    if contract_number is None:
        return None
    cur.execute("INSERT INTO mart.dim_contract (contract_number, company_key) VALUES (%s, %s) ON CONFLICT (contract_number, company_key) DO NOTHING RETURNING contract_key",
                (contract_number, company_key))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("SELECT contract_key FROM mart.dim_contract WHERE contract_number = %s AND company_key = %s", (contract_number, company_key))
    return cur.fetchone()[0]

def upsert_file(cur, file_name, file_checksum):
    cur.execute("INSERT INTO mart.dim_file (file_name, file_checksum, ingested_at) VALUES (%s, %s, now()) ON CONFLICT (file_checksum) DO NOTHING RETURNING file_key",
                (file_name, file_checksum))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("SELECT file_key FROM mart.dim_file WHERE file_checksum = %s", (file_checksum,))
    return cur.fetchone()[0]

def process_file(cur, file_id, file_name, file_checksum, report_date):
    # ensure dim entries
    date_key = ensure_dim_date(cur, report_date)
    file_key = upsert_file(cur, file_name, file_checksum)

    cur.execute("SELECT raw_row_id, row_number, registry_code, contract_number, debt_amount, debt_days, raw_payload FROM staging.raw_debt_rows WHERE file_id = %s", (file_id,))
    rows = cur.fetchall()
    for raw_row_id, row_number, registry_code, contract_number, debt_amount, debt_days, raw_payload in rows:
        company_key = upsert_company(cur, registry_code)
        contract_key = upsert_contract(cur, contract_number, company_key) if company_key is not None else None

        # snapshot_date from file's report_date
        snapshot_date = report_date

        # ensure contract_key exists; if not, skip row
        if contract_key is None:
            LOGGER.info('warning: contract_key is none, skipping fact_debt_snapshot update')
            # write a quality result? for now skip
            continue

        # insert or update fact snapshot
        cur.execute(
            """
            INSERT INTO mart.fact_debt_snapshot (company_key, contract_key, date_key, file_key, snapshot_date, debt_amount, debt_days)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (contract_key, snapshot_date)
            DO UPDATE SET debt_amount = EXCLUDED.debt_amount, debt_days = EXCLUDED.debt_days, file_key = EXCLUDED.file_key
            """,
            (company_key, contract_key, date_key, file_key, snapshot_date, debt_amount if debt_amount is not None else 0, debt_days)
        )

def compute_kpis(cur):
    cur.execute("""
    INSERT INTO mart.kpi_daily_debt (snapshot_date, total_debt_amount, weighted_avg_debt_days, max_debt_days, debt_contract_count, debt_company_count, calculated_at)
    SELECT
        snapshot_date,
        SUM(debt_amount) AS total_debt_amount,
        SUM(CASE WHEN debt_days > 0 THEN debt_days * debt_amount ELSE 0 END)
            / NULLIF(SUM(CASE WHEN debt_days > 0 THEN debt_amount ELSE 0 END), 0)
            AS weighted_avg_debt_days,
        MAX(debt_days) AS max_debt_days,
        COUNT(DISTINCT CASE WHEN debt_days > 0 THEN contract_key END) AS debt_contract_count,
        COUNT(DISTINCT CASE WHEN debt_days > 0 THEN company_key END) AS debt_company_count,
        now()
    FROM mart.fact_debt_snapshot
    GROUP BY snapshot_date
    ON CONFLICT (snapshot_date) DO UPDATE SET
      total_debt_amount = EXCLUDED.total_debt_amount,
      weighted_avg_debt_days = EXCLUDED.weighted_avg_debt_days,
      max_debt_days = EXCLUDED.max_debt_days,
      debt_contract_count = EXCLUDED.debt_contract_count,
      debt_company_count = EXCLUDED.debt_company_count,
      calculated_at = EXCLUDED.calculated_at;
    """)

def do_transform():
    result = attempt_db_connect(LOGGER)
    if result is None or isinstance(result, psycopg2.OperationalError):
        LOGGER.error(result)
        return
    conn = result
    try:
        with conn.cursor() as cur:
            # fetch files marked ingested (or all)
            cur.execute("SELECT file_id, file_name, file_checksum, report_date FROM staging.ingested_files WHERE status = 'ingested' ORDER BY report_date")
            files = cur.fetchall()
            for file_id, file_name, file_checksum, report_date in files:
                try:
                    process_file(cur, file_id, file_name, file_checksum, report_date)
                    # mark file as processed
                    cur.execute("UPDATE staging.ingested_files SET status = 'processed' WHERE file_id = %s", (file_id,))
                    conn.commit()
                except Exception as error:
                    conn.rollback()
                    LOGGER.error(f'Error processing {file_name=}: {error=} {traceback.extract_tb()=}')
            # recompute KPIs
            compute_kpis(cur)
            conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    do_transform()
