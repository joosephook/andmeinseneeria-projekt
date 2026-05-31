import os
import hashlib
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import logging
from utils import attempt_db_connect

LOGGER = logging.getLogger(__file__)

# Configuration via env
ARUANNE_DIR = os.environ.get('ARUANNE_DIR', '/data/aruanne')
TARGET_FILENAME = os.environ.get('TARGET_FILENAME', 'LN002 Laenude võlgnevus.xlsx')

def file_checksum(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return 'sha256:' + h.hexdigest()

def discover_files(base_dir):
    matches = []
    for root, dirs, files in os.walk(base_dir):
        if TARGET_FILENAME in files:
            matches.append(os.path.join(root, TARGET_FILENAME))
    return matches

def map_columns(df):
    # lowercase columns
    cols = {c.lower(): c for c in df.columns}
    # mapping heuristics
    def find(key_sub):
        for k in cols:
            if key_sub in k:
                return cols[k]
        return None

    registry = find('reg.kood') or find('reg') or find('registr')
    contract = (
        find('sap laenulepingu number')
        or find('laenulepingu number')
        or find('laenulepingu nr')
        or find('lepingu')
        or find('contract'))
    amount = find('summa') or find('sum') or find('võlg') or find('debt')
    days = find('ületatud') or find('päevi') or find('võlap') or find('days')

    return registry, contract, amount, days

def truncate(conn):
    with conn.cursor() as cur:
        # insert ingested file
        cur.execute(
            """
            TRUNCATE staging.ingested_files,
            staging.raw_debt_rows,
            staging.ingested_files,
            staging.raw_debt_rows,
            quality.quality_results,
            logs.pipeline_runs,
            mart.dim_company,
            mart.dim_contract,
            mart.dim_date,
            mart.dim_file,
            mart.fact_debt_snapshot,
            mart.kpi_daily_debt
            RESTART IDENTITY
            """,
        )
    conn.commit()
def normalize_registry(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value.endswith(".0"):
        value = value[:-2]

    if not value.isdigit():
        return None

    if len(value) != 8:
        return None

    return value


def normalize_contract(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def normalize_amount(value):
    if pd.isna(value):
        return None

    try:
        value = str(value).replace(",", ".").replace(" ", "").strip()
        amount = float(value)
    except Exception:
        return None

    if amount < 0:
        return None

    return amount


def normalize_days(value):
    if pd.isna(value) or value == "":
        return None

    try:
        days = int(float(str(value).replace(",", ".").strip()))
    except Exception:
        return None

    if days < 0:
        return None

    return days


def add_quality_result(cur, file_id, raw_row_id, rule_code, status, message):
    cur.execute(
        """
        INSERT INTO quality.quality_results
            (file_id, raw_row_id, rule_code, status, message)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (file_id, raw_row_id, rule_code, status, message),
    )


def validate_required_columns(registry_col, contract_col, amount_col):
    missing = []

    if not registry_col:
        missing.append("registrikood")
    if not contract_col:
        missing.append("lepingu number")
    if not amount_col:
        missing.append("võlasumma")

    if missing:
        raise ValueError("Puuduvad kohustuslikud veerud: " + ", ".join(missing))


def ingest_file(conn, path):
    LOGGER.info(f'Ingesting {path=}')

    checksum = file_checksum(path)
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    report_date = (mtime - timedelta(days=1)).date()

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT file_id
            FROM staging.ingested_files
            WHERE file_checksum = %s
            """,
            (checksum,)
        )

        if cur.fetchone():
            LOGGER.info(f"Duplicate file skipped: {path}")
            return

    df = pd.read_excel(path, header=3)
    registry_col, contract_col, amount_col, days_col = map_columns(df)
    
    validate_required_columns(registry_col, contract_col, amount_col)

    with conn.cursor() as cur:
        # insert ingested file
        cur.execute(
            """
            INSERT INTO staging.ingested_files (file_name, file_checksum, source_path, report_date, ingested_at, status)
            VALUES (%s, %s, %s, %s, now(), %s)
            RETURNING file_id
            """,
            (os.path.basename(path), checksum, path, report_date, 'ingested')
        )
        file_id = cur.fetchone()[0]

        # prepare rows
        rows = []
        for idx, row in df.iterrows():
            registry = normalize_registry(row.get(registry_col) if registry_col else None)
            contract = normalize_contract(row.get(contract_col) if contract_col else None)
            amount = normalize_amount(row.get(amount_col) if amount_col else None)
            days = normalize_days(row.get(days_col) if days_col else None)

            if registry is None:
                add_quality_result(cur, file_id, None, 'REGISTRY_CODE', 'FAILED', f'Invalid registry code on row {idx + 1}')
            else:
                add_quality_result(cur, file_id, None, 'REGISTRY_CODE', 'PASSED', f'Valid registry code on row {idx + 1}')

            if contract is None:
                add_quality_result(cur, file_id, None, 'CONTRACT_NUMBER', 'FAILED', f'Missing contract number on row {idx + 1}')
            else:
                add_quality_result(cur, file_id, None, 'CONTRACT_NUMBER', 'PASSED', f'Valid contract number on row {idx + 1}')

            if amount is None:
                add_quality_result(cur, file_id, None, 'DEBT_AMOUNT', 'FAILED', f'Invalid debt amount on row {idx + 1}')
            else:
                add_quality_result(cur, file_id, None, 'DEBT_AMOUNT', 'PASSED', f'Valid debt amount on row {idx + 1}')

            if days is None:
                add_quality_result(cur, file_id, None, 'DEBT_DAYS', 'PASSED', f'Debt days empty or not overdue on row {idx + 1}')
            else:
                add_quality_result(cur, file_id, None, 'DEBT_DAYS', 'PASSED', f'Valid debt days on row {idx + 1}')

            rows.append((file_id, int(idx) + 1, registry, contract, amount, days, None))
        insert_sql = (
            "INSERT INTO staging.raw_debt_rows (file_id, row_number, registry_code, contract_number, debt_amount, debt_days, raw_payload)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cur.executemany(insert_sql, rows)
        conn.commit()
        print(f'Inserted {len(rows)} rows for file_id={file_id}')

def do_ingest():
    files = discover_files(ARUANNE_DIR)
    if not files:
        LOGGER.info('No files found in', ARUANNE_DIR)
        return

    result = attempt_db_connect(LOGGER)
    if result is None or isinstance(result, psycopg2.OperationalError):
        LOGGER.error(result)
        return
    conn = result

    truncate(conn)
    LOGGER.info("Truncating tables...")
    for file in files:
        try:
            ingest_file(conn, file)
        except Exception as error:
            LOGGER.error(f"Error ingesting {file}: {error}")

    conn.close()
    return True

if __name__ == '__main__':
    do_ingest()
