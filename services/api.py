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
    return render_template('chart1.html')

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
