# from telethon.sync import TelegramClient
# from telegram.ext import Updater, CommandHandler
# from telethon.tl.types import InputMessagesFilterRoundVideo,  DocumentAttributeVideo
# from telethon.tl.types import InputMessagesFilterVideo
# from telethon.tl.functions.help import GetUserInfoRequest

# import asyncio



# # Your API ID and Hash obtained from Telegram API registration


# phonNumber = '+3806632103424'  # Your phone number with country code (+1234567890)



# async def fetch_chat_info():
#     with open('chat_id.txt', 'r') as file:
#         chat_id = int(file.read().strip())

#     async with TelegramClient('session_name', api_id, api_hash) as client:
#         try:
#             entity = await client.get_entity(chat_id)
#             print(f"Chat Title: {entity.title}, Chat ID: {entity.id}")
#             return entity
#         except Exception as e:
#             print(f"Error fetching chat ID: {e}")
            




# async def count_video_messages(entity):
#     async with TelegramClient('h', api_id, api_hash) as client:
#         print("ljkjsdk")
#         try:
#             messages = await client.get_messages(entity, limit=None, filter=InputMessagesFilterRoundVideo())
            
#             # Dictionary to store counts of video messages per user
#             video_message_count = {}
#             not_none_messages = (message for message in messages if message.from_id is not None)
#             users = (user_id for message in not_none_messages if (user_id:=message.from_id.user_id) is not None)
#             for user in users:
#                 video_message_count[user] = video_message_count.get(user, 0) + 1
#             # for message in messages:
#             #     if message.from_id is not None:
#             #         user_id = message.from_id.user_id
#             #         # print(user_id)
#             #         if user_id is not None:  # Check if from_id is not None
#             #             if user_id in video_message_count:
#             #                 video_message_count[user_id] += 1
#             #             else:
#             #                 video_message_count[user_id] = 1

#             print("Video Message Counts:")
            
#             for user_id, count in video_message_count.items():
#                 user_entity = await client.get_entity(user_id)
#                 if user_entity:
#                     username = user_entity.username if hasattr(user_entity, 'username') else None
#                     print(f"Username: {username}, Video Message Count: {count}")
#                 else:
#                     print(f"User ID: {user_id},  Video Message Count: {count}")

#         except Exception as e:
#             print(f"Error: {e}")


# async def sum_video_durations(entity):
#     async with TelegramClient('dur', api_id, api_hash) as client:
#         try:
#             messages = await client.get_messages(entity, limit=None, filter=InputMessagesFilterRoundVideo())
            
#             # Dictionary to store total video duration per user
#             video_duration_sum = {}

#             for message in messages:
#                 user_id = message.from_id.user_id if message.from_id else None
#                 if user_id:
#                     if user_id not in video_duration_sum:
#                         video_duration_sum[user_id] = 0
                    
#                     media = message.media
#                     if hasattr(media, 'round_message') and hasattr(media.round_message, 'video'):
#                         video_attr = media.round_message.video
#                         duration = video_attr.duration
#                         video_duration_sum[user_id] += duration

#             print("Total Video Durations per User:")
            
#             for user_id, total_duration in video_duration_sum.items():
#                 user_entity = await client.get_entity(user_id)
#                 if user_entity:
#                     username = user_entity.username if hasattr(user_entity, 'username') else None
#                     print(f"Username: {username}, Total Video Duration: {total_duration} seconds")
#                 else:
#                     print(f"User ID: {user_id}, Total Video Duration: {total_duration} seconds")

#         except Exception as e:
#             print(f"Error: {e}")

# def main():
#     # Telegram bot token obtained from BotFather

#     # Create an Updater object

#     # Get the dispatcher to register handlers

#     # Register a command handler
#     # count_video_messages()
#     ent=asyncio.run(fetch_chat_info())
#     print(ent.id)
#     asyncio.run(count_video_messages(ent))
#     asyncio.run(sum_video_durations(ent))

   
#     # dp.add_handler(CommandHandler("chatInfo", chatInfo))

#     # dp.add_handler(CommandHandler("updatestats", updateStats))
#     # dp.add_handler(CommandHandler("showstats", showStats))


#     # Start the bot

# if __name__ == '__main__':
#     main()
import configparser
import json
import asyncio
from datetime import date, datetime


# import asyncio
import tkinter as tk
from telethon import TelegramClient, errors



# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)
phone=0
username=""
client=0


async def get_code():
    code=code_entry.get()
    psw=password_entry.get()

    print(code)
    try: 
           
            await client.sign_in(phone,code)

    except errors.SessionPasswordNeededError:
               await client.sign_in(password=psw)
    open_new_window()
    me = await client.get_me()
    print(me.stringify())            

# def send_code(phone_number, username,client):
   
    
       
    


async def start_login():
    await client.connect()
    try:
         if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code_entry.pack()
            code_entry.insert(0,"enter code")
            password_entry.pack()
            password_entry.insert(0,"password (if have)")
            code_button.pack()
            print(phone)
            
    except errors.FloodWaitError as e:
        print(f"Too many attempts. Please try after {e.seconds} seconds.")
    except Exception as e:
        print(f"An error occurred: {e}")




def start():
    global phone
    global client
    global username
    phone = phone_entry.get()
    username = username_entry.get()
    client = TelegramClient(username, api_id, api_hash)
    print(client)

    asyncio.get_event_loop().run_until_complete(start_login())  
    print("done")

def verify():
   
  
    # print("Client connected")

    asyncio.get_event_loop().run_until_complete(get_code())  

async def get_chats():
    # Assuming 'client' is your connected TelegramClient instance
    dialogs = await client.get_dialogs()

    chat_list = []
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel or dialog.is_user:
            chat_list.append(dialog.name)

    return chat_list

async def populate_listbox(listbox):
    chat_list = await get_chats()
    listbox.delete(0, tk.END)  # Clear previous items in the listbox
    for chat in chat_list:
        listbox.insert(tk.END, chat)

root = tk.Tk()
root.title("Telegram Login")

# Create a Listbox widget to display chats

# Create a function to fetch chats and populate the Listbox
async def fetch_and_populate(listbox):
    await populate_listbox(listbox)

async def display_chat_info(listbox,info_text):
    info_text.pack()
    selected_index = listbox.curselection()  # Get the index of the selected item
    if selected_index:
        selected_chat_name = listbox.get(selected_index)  # Get the selected chat name
        try:
            async for dialog in client.iter_dialogs():
                if dialog.name == selected_chat_name:
                    info_text.delete(1.0, tk.END)  # Clear previous info
                    info_text.insert(tk.END, f"Chat Name: {dialog.name}\n")
                    info_text.insert(tk.END, f"Chat ID: {dialog.id}\n")
                    # Add more information as needed
        except errors.FloodWaitError as e:
            print(f"Too many attempts. Please try after {e.seconds} seconds.")
        except Exception as e:
            print(f"An error occurred: {e}")

def open_new_window():
    new_window = tk.Toplevel(root)

    new_window.title("New Window")

    label = tk.Label(new_window, text="This is a new window!")
    label.pack()
    listbox = tk.Listbox(new_window)

    listbox.pack()

    fetch_chats_button = tk.Button(new_window, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(listbox)))
    fetch_chats_button.pack()
    info_text = tk.Text(new_window, height=5, width=40)

    get_info_button = tk.Button(new_window, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(listbox,info_text)))
    get_info_button.pack()


# Create the main window


# Create labels, entry, and button
phone_label = tk.Label(root, text="Phone Number:")
phone_label.pack()


username_entry = tk.Entry(root)
username_entry.pack()
username_entry.insert(0,"username")
phone_entry = tk.Entry(root)
phone_entry.pack()
phone_entry.insert(0,"phone number")

code_entry = tk.Entry(root)
password_entry = tk.Entry(root)



login_button = tk.Button(root, text="Login", command=start)
code_button = tk.Button(root, text="Verify",command=verify)

login_button.pack()

# Run the main loop
root.mainloop()

# with client:
#     client.loop.run_until_complete(main(phone))