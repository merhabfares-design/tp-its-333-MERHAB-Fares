import sqlite3

DB_NAME = "database.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            adresse TEXT,
            pincode TEXT
        )
    """)
    conn.commit()
    conn.close()
