import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "censusbd.db")

def get_db():
    conn = sqlite3.connect(db_path)
    return conn

def chk_conn(conn):
     try:
        conn.cursor()
        return True
     except Exception as ex:
        return False