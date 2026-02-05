import sqlite3
from datetime import datetime

DB_NAME = "logs.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            received_at TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL)
""")
    
    conn.commit()
    conn.close()

def insert_logs(log):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logs (timestamp, received_at, service, severity, message)
        VALUES (?, ?, ?, ?, ?)
""", (
    log["timestamp"],
    log["received_at"],
    log["service"],
    log["severity"],
    log["message"]
))
    conn.commit()
    conn.close()
    