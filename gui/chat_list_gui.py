import asyncio
import sqlite3
import tkinter as tk

from db import chats, stats
from gui import login_gui
from src import telegram_client
from telethon import TelegramClient, errors

# from gui import login_gui


# chats_window = tk.Toplevel(telegram_client.root)
lisb = tk.Listbox(telegram_client.root)

fetch_chats_button = tk.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))
info_text = tk.Text(telegram_client.root, height=5, width=40)

get_info_button = tk.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb,info_text)))
chat_list=[]

def open_new_window():
    global lisb  
    global fetch_chats_button  
    global get_info_button  

    telegram_client.root.title("Chat list")

    label = tk.Label(telegram_client.root, text="This is list of your chats, choose one to analyze")
    label.pack()
    lisb = tk.Listbox(telegram_client.root)

    lisb.pack()
    info_text = tk.Text(telegram_client.root, height=5, width=40)
    fetch_chats_button = tk.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))

    get_info_button = tk.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb,info_text)))


    fetch_chats_button.pack()

    get_info_button.pack()
    # telegram_client.root.mainloop()



async def populate_listbox(lb):
    await put_chats_to_db()
    await get_chats()
    # chat_list=[]
    lb.delete(0, tk.END)  # Clear previous items in the listbox
    for chat in chat_list:
        lb.insert(tk.END, chat[0])

# root = tk.Tk()
# root.title("Telegram Login")


async def fetch_and_populate(lb):
    await populate_listbox(lb)

def display_statistics():
    conn = sqlite3.connect('telegram_stats_db.db')
    cursor = conn.cursor()

    # Выбираем все записи из таблицы statistics
    cursor.execute('SELECT * FROM statistics')
    rows = cursor.fetchall()

    # Выводим данные
    for row in rows:
        print(row)

    conn.close()

async def display_chat_info(lb,info_text):
    # info_text.pack()
    selected_index = lb.curselection()  # Get the index of the selected item
    if selected_index:
        selected_chat_name = lb.get(selected_index)  # Get the selected chat name
        for chat in chat_list:
            if chat[0]==selected_chat_name:
                offset_id = 0  # Идентификатор сообщения для смещения
                limit = 100     # Максимальное количество сообщений, возвращаемых за один запрос

                while True:
                    # Получаем порцию сообщений из целевого чата
                    messages = await login_gui.client.get_messages(chat[1], limit=limit, offset_id=offset_id)

                    # Если сообщений нет, завершаем цикл
                    if not messages:
                        break

                    # Собираем статистику для каждого сообщения
                    for message in messages:
                        stats.save_message_statistics(message)

                    # Устанавливаем новое значение offset_id для следующего запроса
                    offset_id = messages[-1].id

                # info_text.delete(1.0, tk.END)  # Clear previous info
                # info_text.insert(tk.END, f"Chat Name: {chat[0]}\n")
                # info_text.insert(tk.END, f"Chat ID: {chat[1]}\n")
    display_statistics()
async def put_chats_to_db():
# Получаем список чатов
    dialogs = await login_gui.client.get_dialogs()

    # Создаем таблицу, если ее нет
    # chats.create_chats_table()

    # Выводим информацию о чатах и сохраняем их в базу данных
    for dialog in dialogs:
        # print(f"Chat ID: {dialog}")

        chats.save_chat_to_db(dialog)


async def get_chats():    
    # Assuming 'client' is your connected TelegramClient instance
    connection = sqlite3.connect('telegram_stats_db.db')
    cursor = connection.cursor()
    cursor.execute('SELECT chat_title, chat_id FROM chats ')
    rows = cursor.fetchall()
    
    global chat_list

    for row in rows:
        chat_list.append((row[0],row[1]))
        # print(row[0])
    connection.commit()
    connection.close()

    # return chat_list       

def clear_form():
    for widget in telegram_client.root.winfo_children():
        widget.destroy()    

