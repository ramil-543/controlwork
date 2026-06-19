import sqlite3
from config import DB_NAME

def add_item(name: str, quantity: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (name, quantity) VALUES (?, ?)", 
            (name, quantity)
        )
        conn.commit()

def get_all_items():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, is_bought FROM items")
        return cursor.fetchall()

def update_item_status(item_id: int, is_bought: bool):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET is_bought = ? WHERE id = ?", 
            (1 if is_bought else 0, item_id)
        )
        conn.commit()

def delete_item(item_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()