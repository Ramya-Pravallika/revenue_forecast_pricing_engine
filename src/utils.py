# utils.py
from pathlib import Path
import sqlite3
import pandas as pd

def read_table(db_path='data/revenue.db', table='sales'):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f'SELECT * FROM {table}', conn, parse_dates=['date'])
    conn.close()
    return df
