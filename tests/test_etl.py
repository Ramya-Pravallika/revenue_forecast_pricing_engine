import os
import sqlite3

def test_database_created():
    assert os.path.exists("data/revenue.db")

def test_tables_exist():
    conn = sqlite3.connect("data/revenue.db")
    cursor = conn.cursor()
    required_tables = ["sales", "products", "customers", "promotions", "market_indicators"]
    for t in required_tables:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{t}'")
        assert cursor.fetchone() is not None
    conn.close()
