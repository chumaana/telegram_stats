"""
Users module

"""
import sqlite3

DB_NAME = "telegram_stats_db.db"


def create_users_table():
    """
    Create users table

    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            phone TEXT,
            name TEXT,
            username TEXT
        )
    ''')

    conn.commit()
    conn.close()