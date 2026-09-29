import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL,
            predicted TEXT NOT NULL,
            chosen TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_checkin(user_id, text, predicted, chosen):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = get_connection()
    conn.execute(
        "INSERT INTO checkins (user_id, created_at, text, predicted, chosen) VALUES (?, ?, ?, ?, ?)",
        (user_id, now, text, predicted, chosen),
    )
    conn.commit()
    conn.close()

def get_all_checkins(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM checkins WHERE user_id = ? ORDER BY id DESC",
                        (user_id,)).fetchall()
    conn.close()
    return rows

def create_user(username, password):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        user_id = None
    conn.close()
    return user_id

def check_login(username, password):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None