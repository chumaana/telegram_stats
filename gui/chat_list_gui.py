"""
GUI module

"""
import asyncio
import sqlite3
import tkinter as tk

import ttkbootstrap as ttb
from db import chats, messages
from gui import login_gui,stats_gui
from src import telegram_client
from telethon.tl.types import User
from ttkbootstrap.constants import *

db_name="telegram_stats_db.db"

lisb = tk.Listbox(telegram_client.root)
label = ttb.Label(telegram_client.root, text="Press to get your chats list",font=("Arial", 12,"bold"))

fetch_chats_button = ttb.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))

get_info_button = ttb.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb)))

chat_list=[]


def open_new_window():
    """
    Configure new window  with fethcing list of chats

    """
    global lisb  
    global fetch_chats_button  
    global get_info_button  
    global label
    telegram_client.root.title("Chat list")
    label = ttb.Label(telegram_client.root, text="Press to get your chats list",font=("Arial", 12,"bold"))

    label.place(relx=0.5, rely=0.5,anchor="center")
    fetch_chats_button = ttb.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))
    
    fetch_chats_button.place(relx=0.5, rely=0.6,anchor="center")
    
    lisb = tk.Listbox(telegram_client.root, height=20, width=30)


async def populate_listbox(lb):
    """
    Fill listbox with chat list

    :param lb: listbox

    """
    await save_chats()
    await get_chats()
    lb.delete(0, tk.END) 
    for chat in chat_list:
        lb.insert(tk.END, chat[0])
   
    get_info_button = ttb.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb)))
    get_info_button.place(relx=0.5, rely=0.71,anchor="center")    


async def fetch_and_populate(lb):
    """
    Fetch all chat list

    :param lb: listbox
    """
    global label
    label.destroy()
    fetch_chats_button.destroy()

    label = ttb.Label(telegram_client.root, text="Loading...",font=("Arial", 12,"bold"))
    label.place(relx=0.5, rely=0.5, anchor="center")

    progressbar = ttb.Progressbar(telegram_client.root, bootstyle="danger-striped", maximum=100,mode="indeterminate",length=200)
    progressbar.place(relx=0.5, rely=0.6, anchor="center")
    progressbar.start(60) 


    task = asyncio.create_task(populate_listbox(lb))
    while not task.done():
        telegram_client.root.update_idletasks()
        await asyncio.sleep(0.1)  
    progressbar.destroy()
    label.destroy()

    label = ttb.Label(telegram_client.root, text="This is list of your chats, choose one to analyze",font=("Arial", 12,"bold"))
    label.place(relx=0.5, rely=0.3,anchor="center")
    lb.place(relx=0.5, rely=0.5,anchor="center")


async def fetch_messages(selected_index,selected_chat_name):
    """
    Select one chat and save to database

    :param lb: listbox
    """
    if selected_index:
        for chat in chat_list:
            if chat[0]==selected_chat_name:

                offset_id = 0  
                limit = 100   

                while True:
                    all_messages = await login_gui.client.get_messages(chat[1], limit=limit, offset_id=offset_id)

                    if not all_messages:
                        break

                    for message in all_messages:
                        messages.save_message_statistics(message)

                    offset_id = all_messages[-1].id

                await save_users(login_gui.client, chat[1])



async def display_chat_info(lb):
    """
    Select one chat and save to database

    :param lb: listbox
    """
    global label
    global label

    # global get_info_button

    # telegram_client.root.destroy()
    # label.destroy()
    # fetch_chats_button.destroy()
    selected_index = lb.curselection()  

    selected_chat_name = lb.get(selected_index) 
    clear_form()
    label = ttb.Label(telegram_client.root, text="Loading...",font=("Arial", 12,"bold"))
    label.place(relx=0.5, rely=0.5, anchor="center")

    progressbar = ttb.Progressbar(telegram_client.root, bootstyle="danger-striped", maximum=100,mode="indeterminate",length=200)
    progressbar.place(relx=0.5, rely=0.6, anchor="center")


    task = asyncio.create_task(fetch_messages(selected_index,selected_chat_name))
    while not task.done():
        telegram_client.root.update_idletasks()
        progressbar.start(60)  # Update the window to display the updated label
        await asyncio.sleep(0.1)  # Adjust the sleep duration as needed

    progressbar.destroy()
    stats_gui.display_stats()


async def save_chats():
    """
    Save chats to database

    """

    dialogs = await login_gui.client.get_dialogs()

    for dialog in dialogs:
        chats.save_chat_to_db(dialog)


async def get_chats():    
    """
    Getting

    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT chat_title, chat_id FROM chats ')
    rows = cursor.fetchall()
    
    global chat_list

    for row in rows:
        chat_list.append((row[0],row[1]))
        # print(row[0])
    connection.commit()
    connection.close()


async def save_users(client, chat_id):
    """
    Save users from selected chat to database

    :param client:
    :param chat_id:
    """
    participants = await client.get_participants(chat_id)
        
    for participant in participants:
        if isinstance(participant, User):
            user_id = participant.id
            phone = participant.phone
            name = participant.first_name + " " + participant.last_name if participant.last_name else participant.first_name
            username = participant.username
               
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            cursor.execute('''
                    INSERT INTO users (user_id, phone, name,username)
                    VALUES (?, ?, ?,?)
            ''', (user_id, phone,name,username))

            conn.commit()
            conn.close()


def clear_form():
    """
    Clear all widgets from the form

    """
    for widget in telegram_client.root.winfo_children():
        widget.destroy()    

