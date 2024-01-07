"""
Messages module

"""
import sqlite3
# from telethon.sync import TelegramClient
from telethon.tl.types import Message
# from telethon.tl import types
from telethon.tl.types import (
    MessageMediaDocument,
    DocumentAttributeVideo,
    DocumentAttributeAudio,
    DocumentAttributeSticker
)

DB_NAME = "telegram_stats_db.db"


def create_messages_table():
    """
    Create messages table

    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            date_sent TEXT,
            message_type TEXT,
            duration double
         )
    ''')

    conn.commit()
    conn.close()


def is_video_document(message_media_document):
    """
    Identify the message type

    :param message_media_document: media parameter
    :return: True if it video document.
    """
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeVideo):
                return True
    return False


def is_audio_document(message_media_document):
    """
    Identify the message type

    :param message_media_document: media parameter
    :return: True if it audio document.
    """
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeAudio):
                return True
    return False


def is_sticker_document(message_media_document):
    """
    Identify the message type

    :param message_media_document: media parameter
    :return: True if it sticker document.
    """
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeSticker):
                return True
    return False


def is_round_video_document(message_media_document):
    """
    Identify the message type

    :param message_media_document: media parameter
    :return: True if it round video document.
    """
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeVideo) and \
                    attribute.round_message:
                return True
    return False


def get_message_type(message: Message):
    """
    Get message type

    :param Message
    :return: message type.
    """
    if message.media and is_round_video_document(message.media):
        return "Round Video"
    if message.media and is_video_document(message.media):
        return "Video"
    if message.media and is_audio_document(message.media):
        return "Audio"
    if message.media and is_sticker_document(message.media):
        return "Sticker"
    if type(message.media).__name__ == 'MessageMediaPhoto':
        return "Photo"
    if message.text:
        return "Text"
    return "Other"


def save_message_statistics(message: Message):
    """
    Save message

    :param Message
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Получаем информацию о сообщении
    user_id = message.from_id.user_id if message.from_id else None
#    chat_id = message.chat_id
    message_type = get_message_type(message)

    date_sent = message.date.strftime("%Y-%m-%d %H:%M:%S")
    duration = None
    if isinstance(message.media, MessageMediaDocument):
        for attribute in message.media.document.attributes:
            if isinstance(attribute,
                          (DocumentAttributeVideo, DocumentAttributeAudio)):
                duration = attribute.duration

    cursor.execute('''
        INSERT INTO messages (user_id, date_sent, message_type, duration)
        VALUES (?, ?, ?, ?)
    ''', (user_id, date_sent, message_type, duration))

    conn.commit()
    conn.close()
