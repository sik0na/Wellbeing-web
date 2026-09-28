import sqlite3
from datetime import datetime

DB_FILE = "wellbeing.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL,
            predicted TEXT NOT NULL,
            chosen TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_checkin(text, predicted, chosen):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_connection()
    conn.execute(
        "INSERT INTO checkins (created_at, text, predicted, chosen) VALUES (?, ?, ?, ?)",
        (now, text, predicted, chosen),
    )
    conn.commit()
    conn.close()

def get_all_checkins():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM checkins ORDER BY id DESC").fetchall()
    return rows