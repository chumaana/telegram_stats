import asyncio
import tkinter as tk
from datetime import datetime, timedelta

import ttkbootstrap as ttb
from db import chats
from gui import login_gui,chat_list_gui
from src import telegram_client,stats
from ttkbootstrap.constants import *
from tkcalendar import Calendar,DateEntry
message_labels = [] 


start_cal=ttb.Entry(telegram_client.root)
end_cal=ttb.Entry(telegram_client.root)
top_label = ttb.Label(telegram_client.root, text="Top message types for the period", font=("Arial", 12,"bold"))
message_label = ttb.Label(telegram_client.root, text=f"", font=("Arial", 10))
label_frequency_per_hour_type=ttb.Label(text="Frequency of messages sent per hour by type", font=("Arial", 12, "bold"))
label_message_frequency_per_hour_type=ttb.Label(text=f"",font=("Arial", 10))
label_frequency_per_hour_type_user=ttb.Label(text="Frequency of messages sent per hour by type and user")
amount_all =ttb.Label(telegram_client.root,text=f"",font=("Arial", 14, "bold"))
label_frequency_per_hour=ttb.Label(text=f"Total frequency of messages sent per hour:")
label_message_frequency_per_hour_type_user=ttb.Label(text=f"", font=("Arial", 10))
container_frame_frequency = ttb.Frame(telegram_client.root)
frequency_frame = ttb.Frame(container_frame_frequency) #,bootstyle="primary"
message_listbox = tk.Listbox(container_frame_frequency, font=("Arial", 10), width=40, height=15)

# start_cal = DateEntry(telegram_client.root,selectmode='day',textvariable=sel)
# end_cal = DateEntry(telegram_client.root,selectmode='day',textvariable=sel1)
start_date=""
end_date=""


def display_general_info():
    all=stats.get_message_amount()
    amount_all =ttb.Label(telegram_client.root,text=f"Messages amount: {all[0]}",font=("Arial", 14, "bold"))
    amount_all.pack(side='top')
    top_messages = stats.get_top_message_types()
    count=0
    top_label = ttb.Label(telegram_client.root, text="Top of messages types", font=("Arial", 12,"bold"))
    top_label.pack()
    for message_info in top_messages:
        count+=1
        message_type = message_info['message_type']
        message_count = message_info['message_count']

        message_label = ttb.Label(telegram_client.root, text=f"{count}. {message_type}: {message_count}", font=("Arial", 10))
        message_label.pack()



# display users and all their messages and types
def display_general_users_info():
    # frame = tk.Frame(telegram_client.root)
    # frame.pack(padx=50, pady=50)
    
    message_statistics = stats.get_message_statistics()

    # frame.title("Message users")

    container_frame = ttb.Frame(telegram_client.root)
    container_frame.pack()
    # container_frame.place( relx=0.5,anchor="center")


    for user_id, message_types in message_statistics.items():
        if user_id != None:
            user_frame = ttb.Frame(container_frame) #,bootstyle="primary"
            user_frame.pack( side='left',padx=30, pady=20)
            labelframe =ttb.Label(user_frame,text=f"User: {stats.get_username_or_phone(user_id)}",style='Primary.TLabel',font=("Arial", 10, "bold"))
            labelframe.pack(side='top')
            # labelframe.place(relx=0.5, rely=0,anchor="center")
            # label = tk.Label(user_frame, text=f"User ID: {user_id}", font=("Arial", 12, "bold"))
            # label.pack()

            text_widget = tk.Text(user_frame, width=20, height=10)
            text_widget.pack()

            text_widget.insert(tk.END, "Message Types\n")
            for message_type_info in message_types:
                text_widget.insert(tk.END, f"{message_type_info['message_type']}: {message_type_info['total_count']}\n")
            text_widget.configure(state="disabled")  # Make text read-only

    
#    display duration of all video and audio messages
def display_audio_and_video_info():
    av_block =ttb.Label(telegram_client.root,text=f"Audio and video statistics",font=("Arial", 14, "bold"))
    av_block.pack(side='top')
    total_duration = stats.get_total_duration()
    container_frame = ttb.Frame(telegram_client.root)
    container_frame.pack()
    if total_duration:
        for user_id, durations in total_duration.items():
            if user_id!=None:
                user_frame = ttb.Frame(container_frame) #,bootstyle="primary"
                user_frame.pack( side='left',padx=10, pady=5)
                user_label = ttb.Label(user_frame, text=f"User: {stats.get_username_or_phone(user_id)}", style='Primary.TLabel',font=("Arial", 10, "bold"))
                user_label.pack(side='top')

                audio_label = ttb.Label(user_frame, text=f"  Audio Duration: {durations['audio_duration']} sec")
                audio_label.pack(side='top')

                video_label = ttb.Label(user_frame, text=f"  Video Duration: {durations['video_duration']} sec")
                video_label.pack(side='top')

def display_frequency():
    global label_frequency_per_hour_type
    global label_message_frequency_per_hour_type
    global label_frequency_per_hour_type_user
    global label_frequency_per_hour
    global label_message_frequency_per_hour_type_user
    global container_frame_frequency
    global frequency_frame

    message_type_frequency_per_hour = stats.get_message_type_frequency_per_hour_nouser(start_date, end_date)
    
# Выводим результат
    # print(f"between {start_date}: {end_date}")
    # label_frequency_per_hour_type.destroy()
    # label_frequency_per_hour_type_user.destroy()
    # label_message_frequency_per_hour_type.destroy()
    label_frequency_per_hour.destroy()
    
    # label_message_frequency_per_hour_type_user.destroy()
    # container_frame_frequency.destroy()
    # container_frame_frequency = ttb.Frame(telegram_client.root)
    # container_frame_frequency.pack()
    # amount_all.destroy()
    frequency_frame = ttb.Frame(container_frame_frequency) #,bootstyle="primary"
    frequency_frame.pack( side='left',padx=30, pady=20)
    label_frequency_per_hour_type=ttb.Label(frequency_frame,text="Frequency of messages sent per hour by type", font=("Arial", 12, "bold"))
    label_frequency_per_hour_type.pack(side='top',pady=10)
    message_listbox = tk.Listbox(frequency_frame, font=("Arial", 10), width=20, height=10)
    message_listbox.pack(side="top") 
    for message_type, frequency in message_type_frequency_per_hour.items():
        message_listbox.insert(tk.END,f"{message_type}: {frequency:.2f} per hour")
        message_listbox.pack(side="top")
        # label_message_frequency_per_hour_type=ttb.Label(frequency_frame,text=f"{message_type}: {frequency:.2f} per hour",font=("Arial", 10))
        # label_message_frequency_per_hour_type.pack(side='top')
        

    message_type_frequency_per_hour = stats.get_message_type_frequency_per_hour(start_date, end_date)

    # Выводим результат
    frequency_frame = ttb.Frame(container_frame_frequency) #,bootstyle="primary"
    frequency_frame.pack( side='left')
    label_frequency_per_hour_type_user=ttb.Label(frequency_frame,text="Frequency of messages sent per hour by type and user", font=("Arial", 12, "bold"))
    message_listbox = tk.Listbox(frequency_frame, font=("Arial", 10), width=35, height=10)
    
    label_frequency_per_hour_type_user.pack(side="top",pady=10)
    for user_id, user_data in message_type_frequency_per_hour.items():
        print(f"User ID: {user_id}")
        if user_id!= None:
            for message_type, frequency in user_data.items():
                message_listbox.insert(tk.END,f"{stats.get_username_or_phone(user_id)} sends {message_type}: {frequency:.2f} per hour")
                message_listbox.pack(side="top")
                # label_message_frequency_per_hour_type_user=ttb.Label(frequency_frame,text=f" {stats.get_username_or_phone(user_id)} sends {message_type}: {frequency:.2f} per hour", font=("Arial", 10))
                # label_message_frequency_per_hour_type_user.pack(side="top")
    
  
    total_frequency_per_hour = stats.get_total_message_frequency_per_hour_all(start_date, end_date)
    label_frequency_per_hour=ttb.Label(telegram_client.root,text=f"Total frequency of messages sent per hour:{total_frequency_per_hour:.2f}", font=("Arial", 12, "bold"))
    label_frequency_per_hour.pack(side='top',pady=10)
    
    # print(f"Общая частота сообщений в час: {total_frequency_per_hour:.2f}")    

def get_selected_date():
    global start_cal
    global end_cal
    global start_date
    global end_date
    global top_label
    global message_listbox
    global container_frame_frequency
    global frequency_frame

    start_date = start_cal.get()
    end_date = end_cal.get()
    # top_label.destroy()
    container_frame_frequency.destroy()

    container_frame_frequency = ttb.Frame(telegram_client.root)
    container_frame_frequency.pack(anchor="center")

    frequency_frame = ttb.Frame(container_frame_frequency)
    frequency_frame.pack(side='left', padx=30, pady=20)

    top_label = ttb.Label(frequency_frame, text="Top message types for the period", font=("Arial", 12, "bold"))
    top_label.pack(side="top",pady=10)

    message_listbox = tk.Listbox(frequency_frame, font=("Arial", 10), width=20, height=10)
    message_listbox.pack(side="top")

    top_messages = stats.get_top_message_types_date(start_date, end_date)
    for count, message_info in enumerate(top_messages, start=1):
        message_type = message_info['message_type']
        message_count = message_info['message_count']
        message_listbox.insert(tk.END, f"{count}. {message_type}: {message_count}")

    display_frequency()



def display_period_stats():
    get_period_label=ttb.Label(telegram_client.root,text=f"Enter period to analyze", style='Primary.TLabel',font=("Arial", 12, "bold"))
    get_period_label.pack(pady=10)

    global start_cal
    global end_cal
    global start_date
    global end_date
    global top_label

    start_cal=ttb.Entry(telegram_client.root)
    end_cal=ttb.Entry(telegram_client.root)
    start_cal.pack(pady=5)
    end_cal.pack(pady=5)
    start_cal.insert(0,"start date: '2024-01-03'")
    end_cal.insert(0,"end date: '2024-01-03'")

    
    

    # end_cal.pack(padx=10, pady=10)
    # sel.trace('w',start_upd) 
    # sel1.trace('w',end_upd) 

# Button to get the selected date
    get_date_button = tk.Button(telegram_client.root, text="Selecte Date", command=get_selected_date)
    get_date_button.pack(padx=10, pady=5)
    top_label = ttb.Label(telegram_client.root, text="Top message types for the period", font=("Arial", 12,"bold"))
   

# # from gui import login_gui
def display_stats():
    
    chat_list_gui.clear_form()

    telegram_client.root
    telegram_client.root.title()
    display_general_info() 
    display_general_users_info()
    display_audio_and_video_info() 
    display_period_stats()


    # label = tk.Label(telegram_client.root, text="stats")
    # label.place(relx=0.5, rely=0.3,anchor="center")


# # chats_window = tk.Toplevel(telegram_client.root)
# # lisb = tk.Listbox(telegram_client.root)

# fetch_chats_button = ttb.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))
# info_text = ttb.Text(telegram_client.root, height=5, width=40)

# get_info_button = tk.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb,info_text)))
# chat_list=[]

# def open_new_window():
#     global lisb  
#     global fetch_chats_button  
#     global get_info_button  

#     telegram_client.root.title("Chat list")

#     label = tk.Label(telegram_client.root, text="This is list of your chats, choose one to analyze")
#     label.pack()
#     lisb = tk.Listbox(telegram_client.root)

#     lisb.pack()
#     info_text = tk.Text(telegram_client.root, height=5, width=40)
#     fetch_chats_button = tk.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))

#     get_info_button = tk.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb,info_text)))


#     fetch_chats_button.pack()

#     get_info_button.pack()
#     # telegram_client.root.mainloop()



# async def populate_listbox(lb):
#     await put_chats_to_db()
#     await get_chats()
#     # chat_list=[]
#     lb.delete(0, tk.END)  # Clear previous items in the listbox
#     for chat in chat_list:
#         lb.insert(tk.END, chat[0])

# # root = tk.Tk()
# # root.title("Telegram Login")


# async def fetch_and_populate(lb):
#     await populate_listbox(lb)

# async def display_chat_info(lb,info_text):
#     info_text.pack()
#     selected_index = lb.curselection()  # Get the index of the selected item
#     if selected_index:
#         selected_chat_name = lb.get(selected_index)  # Get the selected chat name
#         for chat in chat_list:
#             if chat[0]==selected_chat_name:

#                 info_text.delete(1.0, tk.END)  # Clear previous info
#                 info_text.insert(tk.END, f"Chat Name: {chat[0]}\n")
#                 info_text.insert(tk.END, f"Chat ID: {chat[1]}\n")

# async def put_chats_to_db():
# # Получаем список чатов
#     dialogs = await login_gui.client.get_dialogs()

#     # Создаем таблицу, если ее нет
#     chats.create_chats_table()

#     # Выводим информацию о чатах и сохраняем их в базу данных
#     for dialog in dialogs:
#         # print(f"Chat ID: {dialog}")

#         chats.save_chat_to_db(dialog)


# async def get_chats():    
#     # Assuming 'client' is your connected TelegramClient instance
#     connection = sqlite3.connect('telegram_stats_db.db')
#     cursor = connection.cursor()
#     cursor.execute('SELECT chat_title, chat_id FROM chats ')
#     rows = cursor.fetchall()
    
#     global chat_list

#     for row in rows:
#         chat_list.append((row[0],row[1]))
#         # print(row[0])
#     connection.commit()
#     connection.close()

#     # return chat_list       

# def clear_form():
#     for widget in telegram_client.root.winfo_children():
#         widget.destroy()    
