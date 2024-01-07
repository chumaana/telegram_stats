"""
sTATS GUI module

"""
import tkinter as tk
from datetime import datetime

import ttkbootstrap as ttb
# from db import chats
from gui import chat_list_gui
from src import stats, telegram_client
# from ttkbootstrap.constants import *

start_cal = ttb.Entry(telegram_client.root)
end_cal = ttb.Entry(telegram_client.root)
top_label = ttb.Label(telegram_client.root, text="Top message types for the period", font=("Arial", 12, "bold"))
label_frequency_per_hour = ttb.Label(text="Total frequency of messages sent per hour:")
container_frame_frequency = ttb.Frame(telegram_client.root)
frequency_frame = ttb.Frame(container_frame_frequency)
# ,bootstyle="primary"
label_error_format = ttb.Label(telegram_client.root, text="Incorect format")
get_period_label = ttb.Label(telegram_client.root, text="Enter period to analyze", style='Primary.TLabel', font=("Arial", 12, "bold"))

start_date = ""
end_date = ""


def display_general_info():
    """
    Display general ino

    """
    all = stats.get_message_amount()
    amount_all = ttb.Label(telegram_client.root, text=f"Messages amount: {all[0]}", font=("Arial", 14, "bold"))
    amount_all.pack(side='top')
    top_messages = stats.get_top_message_types()
    count = 0
    top_label = ttb.Label(telegram_client.root, text="Top of messages types", font=("Arial", 12, "bold"))
    top_label.pack()
    for message_info in top_messages:
        count+=1
        message_type = message_info['message_type']
        message_count = message_info['message_count']

        message_label = ttb.Label(telegram_client.root, text=f"{count}. {message_type}: {message_count}", font=("Arial", 10))
        message_label.pack()


def display_general_users_info():
    """
    Display users and all their messages and types

    """
    message_statistics = stats.get_message_statistics()

    container_frame = ttb.Frame(telegram_client.root)
    container_frame.pack()

    for user_id, message_types in message_statistics.items():
        if user_id is not None:
            user_frame = ttb.Frame(container_frame)
            # ,bootstyle="primary"
            user_frame.pack(side='left', padx=30, pady=20)
            labelframe = ttb.Label(user_frame, text=f"User: {stats.get_username_or_phone(user_id)}, user_id={user_id}", style='Primary.TLabel', font=("Arial", 10, "bold"))
            labelframe.pack(side='top')

            text_widget = tk.Text(user_frame, width=20, height=10)
            text_widget.pack()
            text_widget.insert(tk.END, "Message Types\n")
            for message_type_info in message_types:
                text_widget.insert(tk.END, f"{message_type_info['message_type']}: {message_type_info['total_count']}\n")
            text_widget.configure(state="disabled")  # Make text read-only


def display_audio_and_video_info():
    """
    Display duration of all video and audio messages

    :param lb: listbox
    """
    av_block = ttb.Label(telegram_client.root, text=f"Audio and video statistics", font=("Arial", 14, "bold"))
    av_block.pack(side='top')

    total_duration = stats.get_total_duration()

    container_frame = ttb.Frame(telegram_client.root)
    container_frame.pack()
    if total_duration:
        for user_id, durations in total_duration.items():
            if user_id is not None:
                user_frame = ttb.Frame(container_frame)
                # ,bootstyle="primary"
                user_frame.pack(side='left', padx=10, pady=5)
                user_label = ttb.Label(user_frame, text=f"User: {stats.get_username_or_phone(user_id)}", style='Primary.TLabel', font=("Arial", 10, "bold"))
                user_label.pack(side='top')

                audio_label = ttb.Label(user_frame, text=f"  Audio Duration: {durations['audio_duration']} sec")
                audio_label.pack(side='top')

                video_label = ttb.Label(user_frame, text=f"  Video Duration: {durations['video_duration']} sec")
                video_label.pack(side='top')


def display_frequency():
    """
    Display frequency of sending messages distincted by type (and not) for
    each user(and in general) (per hour per period)

    """
    global label_frequency_per_hour
    global container_frame_frequency
    global frequency_frame

    message_type_frequency_per_hour = stats.get_message_type_frequency_per_hour_nouser(start_date, end_date)

    label_frequency_per_hour.destroy()

    frequency_frame = ttb.Frame(container_frame_frequency)
    # ,bootstyle="primary"
    frequency_frame.pack(side='left', padx=30, pady=20)

    label_frequency_per_hour_type = ttb.Label(frequency_frame, text="Frequency of messages sent per hour by type", font=("Arial", 12, "bold"))
    label_frequency_per_hour_type.pack(side='top', pady=10)

    message_listbox = tk.Listbox(frequency_frame, font=("Arial", 10), width=20, height=10)
    message_listbox.pack(side="top")
    for message_type, frequency in message_type_frequency_per_hour.items():
        message_listbox.insert(tk.END, f"{message_type}: {frequency:.2f} per hour")
        message_listbox.pack(side="top")

    message_type_frequency_per_hour = stats.get_message_type_frequency_per_hour(start_date, end_date)

    frequency_frame = ttb.Frame(container_frame_frequency)
    # ,bootstyle="primary"
    frequency_frame.pack(side='left')

    label_frequency_per_hour_type_user = ttb.Label(frequency_frame, text="Frequency of messages sent per hour by type and user", font=("Arial", 12, "bold"))
    label_frequency_per_hour_type_user.pack(side="top", pady=10)

    message_listbox = tk.Listbox(frequency_frame, font=("Arial", 10), width=35, height=10)

    for user_id, user_data in message_type_frequency_per_hour.items():
        print(f"User ID: {user_id}")
        if user_id is not None:
            for message_type, frequency in user_data.items():
                message_listbox.insert(tk.END, f"{stats.get_username_or_phone(user_id)} sends {message_type}: {frequency:.2f} per hour")
                message_listbox.pack(side="top")

    total_frequency_per_hour = stats.get_total_message_frequency_per_hour_all(start_date, end_date)
    label_frequency_per_hour = ttb.Label(telegram_client.root, text=f"Total frequency of messages sent per hour:{total_frequency_per_hour:.2f}", font=("Arial", 12, "bold"))
    label_frequency_per_hour.pack(side='top', pady=10)


def validate_date(start, end):
    """
    Validate date

    :param start: from
    :param end: to
    :return: True if it valide date.
    """
    global label_error_format
    if label_error_format:
        label_error_format.destroy()

    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")

        if start > end:
            label_error_format = ttb.Label(telegram_client.root, text="Start date should be before end date")
            label_error_format.pack()
            return False

        return True

    except ValueError:
        label_error_format = ttb.Label(telegram_client.root, text="Incorrect date format")
        label_error_format.pack()
        return False


def get_selected_date():
    """
    Get date from input and diplay top message types for the period

    """
    global start_cal
    global end_cal
    global start_date
    global end_date
    global top_label
    global message_listbox
    global container_frame_frequency
    global frequency_frame
    global label_error_format
    label_error_format.destroy()
    start_date = start_cal.get()
    end_date = end_cal.get()
    if validate_date(start_date, end_date):
        container_frame_frequency.destroy()
        container_frame_frequency = ttb.Frame(telegram_client.root)
        container_frame_frequency.pack(anchor="center")

        frequency_frame = ttb.Frame(container_frame_frequency)
        frequency_frame.pack(side='left', padx=30, pady=20)

        top_label = ttb.Label(frequency_frame, text="Top message types for the period", font=("Arial", 12, "bold"))
        top_label.pack(side="top", pady=10)

        message_listbox = tk.Listbox(frequency_frame, font=("Arial", 10), width=20, height=10)
        message_listbox.pack(side="top")

        top_messages = stats.get_top_message_types_date(start_date, end_date)
        for count, message_info in enumerate(top_messages, start=1):
            message_type = message_info['message_type']
            message_count = message_info['message_count']
            message_listbox.insert(tk.END, f"{count}. {message_type}: {message_count}")

        display_frequency()
    # else:
    #     display_period_stats()


def display_period_stats():
    """
    Main function for displaying statistics per period

    """
    global get_period_label
    global start_cal
    global end_cal

    # get_period_label.destroy()
    # start_cal.destroy()
    # end_cal.destroy()

    get_period_label = ttb.Label(telegram_client.root, text=f"Enter period to analyze", style='Primary.TLabel', font=("Arial", 12, "bold"))
    get_period_label.pack(pady=10)

    global start_date
    global end_date
    global top_label

    start_cal = ttb.Entry(telegram_client.root)
    end_cal = ttb.Entry(telegram_client.root)
    start_cal.pack(pady=5)
    end_cal.pack(pady=5)
    start_cal.insert(0, "start date: '2024-01-03'")
    end_cal.insert(0, "end date: '2024-01-03'")

    get_date_button = tk.Button(telegram_client.root, text="Selecte Date", command=get_selected_date)
    get_date_button.pack(padx=10, pady=5)

    top_label = ttb.Label(telegram_client.root, text="Top message types for the period", font=("Arial", 12, "bold"))


def display_stats():
    """
    Main function  displaying all statistics

    """
    chat_list_gui.clear_form()
    # chat_name=stats.get_chat_name()
    telegram_client.root
    telegram_client.root.title("Stistics")

    display_general_info()
    display_general_users_info()
    display_audio_and_video_info()
    display_period_stats()
