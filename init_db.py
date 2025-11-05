import sqlite3
import os

DB_FILE = 'salesDatabase.db'

def initialize_database():
    if os.path.exists(DB_FILE):
        print("database file already exists")
        return

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE sales (
                   sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sale_date TEXT NOT NULL,
                   part_name TEXT NOT NULL
                   )
    """)

    conn.commit()

    print(f"Database {DB_FILE} and table 'sales' created successfully.")

if __name__ == "__main__":
    initialize_database()