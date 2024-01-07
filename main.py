"""
Main module

"""
import sqlite3

from db import chats, messages, users
from gui import login_gui


def clear_table():
    """
    Delete all records from tables

    """
    conn = sqlite3.connect('telegram_stats_db.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM messages')
    cursor.execute('DELETE FROM chats')
    cursor.execute('DELETE FROM users')

    conn.commit()
    conn.close()


def main():
    """
    Main function to initialize necessary tables and launch login GUI

    """
    clear_table()
    chats.create_chats_table()
    messages.create_messages_table()
    users.create_users_table()
    login_gui.create_login_window()



if __name__ == "__main__":
    main()
