import sqlite3
from config import DB_NAME

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                is_bought INTEGER DEFAULT 0
            )
        """)
        conn.commit()