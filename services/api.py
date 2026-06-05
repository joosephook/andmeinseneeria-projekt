from flask import Flask
from flask import jsonify
from flask import render_template
from utils import attempt_db_connect
import sys

import logging
import psycopg2
LOGGER = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler('logs/api.log'),logging.StreamHandler(sys.stdout)] )

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/chart1')
def chart1():
    return render_template('chart1.html')

@app.route('/chart2')
def chart2():
    return render_template('chart2.html')

@app.route('/overdues_report')
def overdues_report():
    return render_template('overdues_report.html')

@app.route('/overdues_summary')
def overdues_summary():
    result = attempt_db_connect(LOGGER)
    if result is None or isinstance(result, psycopg2.OperationalError):
        LOGGER.error(result)
        return str(result)

    conn = result
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT
                snapshot_date,
                weighted_avg_debtdays
            FROM mart.v_overdues_summary
            ORDER BY snapshot_date
            """)
            records = [
                dict(report_date=date,weighted_avg_debtdays=days)
                for date,days
                in cur.fetchall()
            ]
    finally:
        conn.close()
    return jsonify(records)


@app.route('/overdues_counts')
def overdues_counts():
    result = attempt_db_connect(LOGGER)
    if result is None or isinstance(result, psycopg2.OperationalError):
        LOGGER.error(result)
        return str(result)

    conn = result
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT
                snapshot_date,
                company_count,
                contract_count
            FROM mart.v_overdues_counts
            ORDER BY snapshot_date;
            """)
            records = [
                dict(report_date=date,company_count=company_count,contract_count=contract_count)
                for date,company_count,contract_count
                in cur.fetchall()
            ]
    finally:
        conn.close()
    return jsonify(records)

@app.route('/overdues_data')
def overdues_data():
    result = attempt_db_connect(LOGGER)
    if result is None or isinstance(result, psycopg2.OperationalError):
        LOGGER.error(result)
        return str(result)

    conn = result
    try:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT
                col_nr,
                snapshot_date,
                snapshot_date_label
            FROM mart.v_overdues_last5_dates
            ORDER BY col_nr;
            """)
            dates = [
                dict(col_nr=nr,report_date=date,report_date_label=date_label)
                for nr,date,date_label
                in cur.fetchall()
            ]
            cur.execute("""
            SELECT
                registry_code,
                value_1,
                value_2,
                value_3,
                value_4,
                value_5
            FROM mart.v_overdues_company_pivot_last5
            ORDER BY registry_code;
            """)
            rows = [
                dict(company_code=code, value_1=a,value_2=b,value_3=c,value_4=d,value_5=e)
                for code,a,b,c,d,e
                in cur.fetchall()
            ]
    finally:
        conn.close()
    return jsonify(dict(dates=dates,rows=rows))



