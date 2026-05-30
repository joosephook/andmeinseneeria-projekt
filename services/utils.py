import psycopg2
import os
import time
import logging

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'debtdb')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')


def attempt_db_connect(logger: logging.Logger, retries: int = 10):
    wait_for_seconds = 1
    last_error = None
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT,
                    dbname=POSTGRES_DB,
                    user=POSTGRES_USER,
                    password=POSTGRES_PASSWORD
            )
            logger.info('DB connection established')
            conn.autocommit = False
            return conn
        except psycopg2.OperationalError as error:
            last_error = error
            logger.info(f'attempt #{attempt+1} failed when connecting to db, sleeping for {wait_for_seconds}...')
            time.sleep(wait_for_seconds)
            wait_for_seconds += wait_for_seconds
    return last_error
