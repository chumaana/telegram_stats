# import sys
# sys.path.append('../gui')

import asyncio
import configparser
import tkinter as tk

import ttkbootstrap as ttb
from telethon import TelegramClient, errors
from ttkbootstrap.constants import *

# from gui import chat_list_gui
# from gui import login_gui
# from gui import get_verification_data

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))


config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)
phone=0
username=""
root = tk.Tk()
root.attributes('-fullscreen', True)
style= ttb.Style(theme="darkly")
style.theme_use()
# frame = tk.Frame(root)
# frame = ttb.Frame(root, style='My.TFrame')
# frame.pack(expand=True, fill='both')
# frame.place(relx=0.5, rely=0.5, anchor='center')
root.bind("<Escape>", toggle_fullscreen)  # Bind Escape key to toggle fullscreen

toggle_fullscreen()
phone_entry = ttb.Entry(root)
code_entry = ttb.Entry(root)
# code_entry.place(relx=0.5, rely=0.4, anchor='center')
password_entry = ttb.Entry(root)
# password_entry.place(relx=0.5, rely=0.5, anchor='center')
username_entry = ttb.Entry(root)
# username_entry.place(relx=0.5, rely=0.6, anchor='center')
# client = 0

# def get_client():
#     global client  
#     client = TelegramClient(username, api_id, api_hash)
    
# async def start_login():
#     await client.connect()
#     try:
#          if not await client.is_user_authorized():
#             await client.send_code_request(phone)
#             login_gui.expand_login_window()
#             chat_list_gui(phone)
            
#     except errors.FloodWaitError as e:
#         print(f"Too many attempts. Please try after {e.seconds} seconds.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# def start():
#     global phone
#     global client
#     global username
#     phone,username=login_gui.get_login_data()
#     client = TelegramClient(username, api_id, api_hash)
#     print(client)

#     asyncio.get_event_loop().run_until_complete(start_login())  
#     print("done")

# async def get_code():
#     code,psw=login_gui.get_verification_data()
#     print(code)
#     try: 
           
#             await client.sign_in(phone,code)
             
#     except errors.SessionPasswordNeededError:
#                await client.sign_in(password=psw)
               
#     login_gui.open_new_window()
#     me = await client.get_me()
#     print(me.stringify())            

    
# def verify():
   
  
#     # print("Client connected")

#     asyncio.get_event_loop().run_until_complete(get_code())      


# async def populate_listbox(listbox):
#     chat_list = await get_chats()
#     listbox.delete(0, tk.END)  # Clear previous items in the listbox
#     for chat in chat_list:
#         listbox.insert(tk.END, chat)



# Create a Listbox widget to display chats

# Create a function to fetch chats and populate the Listbox


    

