import sqlite3
DATABASE_NAME = "censusbd.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def chk_conn(conn):
     try:
        conn.cursor()
        return True
     except Exception as ex:
        return False