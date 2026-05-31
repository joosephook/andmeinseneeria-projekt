# -*- coding: utf-8 -*-
"""
Created on Sat May 30 23:39:58 2026

"""

import os
from datetime import datetime
import pandas as pd
import psycopg


# ============================================================
# 1. SEADISTUSED
# ============================================================

xlsx_path = r"C:\Users\jaan.soots\Documents\IT\Aruandlus\Võlgnevused\aruanne\LN002 Laenude võlgnevus.xlsx"

db_config = {
    "host": "10.15.0.15",
    "port": 5432,
    "dbname": "postgres",
    "user": "jaan",
    "password": "JaaniPASS",
    "connect_timeout": 5
}


# ============================================================
# 2. FAILI DATE MODIFIED KUUPÄEV
# ============================================================

modified_timestamp = os.path.getmtime(xlsx_path)
report_date = datetime.fromtimestamp(modified_timestamp).date()

print(f"Faili Date modified kuupäev: {report_date}")


# ============================================================
# 3. EXCELI LUGEMINE
# ============================================================

# Exceli veerud:
# 2. veerg  -> indeks 1 -> company_code
# 4. veerg  -> indeks 3 -> sap_contract
# 7. veerg  -> indeks 6 -> debtsum
# 14. veerg -> indeks 13 -> debtdays
#
# Andmed algavad 5. reast.
# skiprows=4 jätab esimesed 4 rida vahele.
# header=None tähendab, et 5. rida on juba andmerida, mitte päiserida.

df = pd.read_excel(
    xlsx_path,
    sheet_name=0,
    header=None,
    skiprows=4,
    usecols=[1, 3, 6, 13],
    dtype=str
)

df.columns = [
    "company_code",
    "sap_contract",
    "debtsum",
    "debtdays"
]

# Tühjad Exceli lahtrid -> tühi string
df = df.fillna("")

# Eemaldame alguse/lõpu tühikud
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# Eemaldame read, kus kõik 4 loetud välja on tühjad
df = df[
    ~(
        (df["company_code"] == "") &
        (df["sap_contract"] == "") &
        (df["debtsum"] == "") &
        (df["debtdays"] == "")
    )
]

# Lisame report_date veeru faili Date modified kuupäevaga
df["report_date"] = report_date

print(f"Excelist loeti andmeridu: {len(df)}")

if len(df) == 0:
    raise ValueError("Excelist ei leitud ühtegi andmerida. Kontrolli skiprows ja usecols seadeid.")


# ============================================================
# 4. ANDMEBAASI KIRJUTAMINE
# ============================================================

try:
    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:

            print("Ühendus PostgreSQL baasiga loodud.")

            # ------------------------------------------------
            # 4.1 Puhastame staging tabeli
            # ------------------------------------------------

            cur.execute("""
                TRUNCATE TABLE reports.overdues_stg RESTART IDENTITY;
            """)

            print("Staging tabel puhastatud.")

            # ------------------------------------------------
            # 4.2 Kirjutame Exceli read staging tabelisse
            # ------------------------------------------------

            insert_stg_sql = """
                INSERT INTO reports.overdues_stg (
                    company_code,
                    sap_contract,
                    debtsum,
                    debtdays,
                    report_date
                )
                VALUES (%s, %s, %s, %s, %s);
            """

            rows = [
                (
                    row["company_code"],
                    row["sap_contract"],
                    row["debtsum"],
                    row["debtdays"],
                    row["report_date"]
                )
                for _, row in df.iterrows()
            ]

            cur.executemany(insert_stg_sql, rows)

            cur.execute("SELECT COUNT(*) FROM reports.overdues_stg;")
            stg_count = cur.fetchone()[0]

            print(f"Staging tabelisse kirjutati ridu: {stg_count}")

            # ------------------------------------------------
            # 4.3 Kustutame püsitabelist sama report_date vanad read
            # ------------------------------------------------

            cur.execute("""
                DELETE FROM reports.overdues
                WHERE report_date IN (
                    SELECT DISTINCT report_date
                    FROM reports.overdues_stg
                );
            """)

            deleted_count = cur.rowcount

            print(f"Püsitabelist kustutati sama kuupäeva vanu ridu: {deleted_count}")

            # ------------------------------------------------
            # 4.4 Tõstame stagingust püsitabelisse
            # ------------------------------------------------

            cur.execute("""
                INSERT INTO reports.overdues (
                    company_code,
                    sap_contract,
                    debtsum,
                    debtdays,
                    report_date
                )
                SELECT
                    company_code::integer,
                    sap_contract::integer,
                    replace(debtsum, ',', '.')::numeric(12,2),
                    NULLIF(debtdays, '')::integer,
                    report_date
                FROM reports.overdues_stg;
            """)

            inserted_count = cur.rowcount

            print(f"Püsitabelisse lisati ridu: {inserted_count}")

            # ------------------------------------------------
            # 4.5 Kontrollkokkuvõte püsitabelist
            # ------------------------------------------------

            cur.execute("""
                SELECT 
                    report_date,
                    COUNT(*) AS row_count,
                    SUM(debtsum) AS total_debtsum
                FROM reports.overdues
                WHERE report_date = %s
                GROUP BY report_date;
            """, (report_date,))

            result = cur.fetchone()

            if result:
                print("Kontroll püsitabelist:")
                print(f"report_date: {result[0]}")
                print(f"ridade arv: {result[1]}")
                print(f"võlasumma kokku: {result[2]}")
            else:
                print("Hoiatus: püsitabelist ei leitud selle report_date kohta ridu.")

    print("Import valmis.")

except Exception as e:
    print("Import ebaõnnestus.")
    print(type(e).__name__)
    print(e)
    raise

