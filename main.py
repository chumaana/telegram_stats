
import configparser
import sqlite3

from gui import login_gui
from db import chats,stats

# from gui.chat_list_window import create_chat_list_window
def clear_table():
    conn = sqlite3.connect('telegram_stats_db.db')
    cursor = conn.cursor()

    # Удаляем все записи из таблицы types
    cursor.execute('DELETE FROM statistics')
    cursor.execute('DELETE FROM chats')

    conn.commit()
    conn.close()

def main():
    # config = configparser.ConfigParser()
    # config.read("config.ini")

    # api_id = config['Telegram']['api_id']
    # api_hash = config['Telegram']['api_hash']
    chats.create_chats_table()
    stats.create_statistics_table()

    login_gui.create_login_window()
    print("end")
    clear_table()
  


    # If login successful, open the chat list window
    # if login_successful:
    #     create_chat_list_window(get_chats)

if __name__ == "__main__":
    main()
