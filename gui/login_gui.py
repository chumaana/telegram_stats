"""
Login GUI module

"""
import asyncio
import tkinter as tk
import ttkbootstrap as ttb
from ttkbootstrap.constants import *

from src import telegram_client
from gui import chat_list_gui
from telethon import TelegramClient, errors


async def start_login():
    """
    Check auth data

    """
    await client.connect()
    try:
         if not await client.is_user_authorized():
            await client.send_code_request(phone)
            expand_login_window()
         else:
            chat_list_gui.clear_form()
            chat_list_gui.open_new_window()

    except errors.FloodWaitError as e:
        print(f"Too many attempts. Please try after {e.seconds} seconds.")
    except Exception as e:
        print(f"An error occurred: {e}")


def start():
    """
    Start session with given phone number

    """
    global phone
    global client
    global username
    phone, username=get_login_data()
    client = TelegramClient(username, telegram_client.api_id, telegram_client.api_hash)
    print(client)

    asyncio.get_event_loop().run_until_complete(start_login())  
    print("done")

async def get_code():
    """
    Get code

    """
    code,psw=get_verification_data()
    print(code)
    try: 
            await client.sign_in(phone,code)
             
    except errors.SessionPasswordNeededError:
               await client.sign_in(password=psw)
               
    chat_list_gui.clear_form()
    chat_list_gui.open_new_window()
    me = await client.get_me()
    print(me.stringify())            

    
def verify():
    """
    Verify

    """

    asyncio.get_event_loop().run_until_complete(get_code())      


def create_login_window():
    """
    Create login window

    """     
    telegram_client.root.title("Telegram Login")

    phone_label = ttb.Label(telegram_client.root, text="Log in:",font=("Arial", 12,"bold"))
    # phone_label.pack()
    phone_label.place(relx=0.5, rely=0.4,anchor="center")


    telegram_client.phone_entry.place(relx=0.5, rely=0.45,anchor="center")
    telegram_client.username_entry.place(relx=0.5, rely=0.5,anchor="center")

    # telegram_client.username_entry.pack()
    telegram_client.username_entry.insert(0,"pitopl")
    # telegram_client.phone_entry.pack()
    telegram_client.phone_entry.insert(0,"+380663210324")




    login_button = ttb.Button(telegram_client.root, text="Login", command=start)
    
    login_button.place(relx=0.5, rely=0.55,anchor="center")

    telegram_client.root.mainloop()

def expand_login_window():
    """
    Expand login window

    """
    telegram_client.code_entry.place(relx=0.5, rely=0.6,anchor="center")
    telegram_client.code_entry.insert(0,"enter code")
    telegram_client.password_entry.place(relx=0.5, rely=0.65,anchor="center")
    telegram_client.password_entry.insert(0,"password (if have)")
    code_button.place(relx=0.5, rely=0.7,anchor="center")


def get_verification_data():
    """
    Configure new window  with fethcing list of chats

    :return: code, psw
    """

    code=telegram_client.code_entry.get()
    psw=telegram_client.password_entry.get()
    return code,psw

def get_login_data():
    """
    Configure new window  with fethcing list of chats

    :return: phone, username
    """
    phone = telegram_client.phone_entry.get()
    username = telegram_client.username_entry.get()
    return phone,username


code_button = tk.Button(telegram_client.root, text="Verify",command=verify)

