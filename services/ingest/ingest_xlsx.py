import os
import hashlib
import psycopg2
import pandas as pd
from datetime import datetime, timedelta

# Configuration via env
ARUANNE_DIR = os.environ.get('ARUANNE_DIR', '/data/aruanne')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'debtdb')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

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

    registry = find('reg') or find('registr') or find('registry_code')
    contract = find('lepingu') or find('contract')
    amount = find('sum') or find('debt')
    days = find('võlap') or find('päev') or find('days')

    return registry, contract, amount, days

def ingest_file(conn, path):
    print('Ingesting', path)
    checksum = file_checksum(path)
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    report_date = (mtime - timedelta(days=1)).date()

    df = pd.read_excel(path)
    registry_col, contract_col, amount_col, days_col = map_columns(df)

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
            registry = row.get(registry_col) if registry_col else None
            contract = row.get(contract_col) if contract_col else None
            amount = row.get(amount_col) if amount_col else None
            days = row.get(days_col) if days_col else None
            # normalize NaN to None
            if pd.isna(registry): registry = None
            if pd.isna(contract): contract = None
            if pd.isna(amount): amount = None
            if pd.isna(days): days = None

            rows.append((file_id, int(idx)+1, registry, contract, amount, days, None))

        insert_sql = (
            "INSERT INTO staging.raw_debt_rows (file_id, row_number, registry_code, contract_number, debt_amount, debt_days, raw_payload)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cur.executemany(insert_sql, rows)
        conn.commit()
        print(f'Inserted {len(rows)} rows for file_id={file_id}')

def main():
    files = discover_files(ARUANNE_DIR)
    if not files:
        print('No files found in', ARUANNE_DIR)
        return

    conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DB,
                            user=POSTGRES_USER, password=POSTGRES_PASSWORD)
    for f in files:
        try:
            ingest_file(conn, f)
        except Exception as e:
            print('Error ingesting', f, e)

    conn.close()

if __name__ == '__main__':
    main()
