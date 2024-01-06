import sqlite3
from telethon.sync import TelegramClient
from telethon.tl.types import Message
from telethon.tl import types
from telethon.tl.types import MessageMediaDocument, DocumentAttributeVideo,DocumentAttributeRoundVideo, DocumentAttributeAudio, DocumentAttributeSticker


def create_statistics_table():
    conn = sqlite3.connect('telegram_stats_db.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            message_type TEXT,
            count INTEGER
        )
    ''')

    conn.commit()
    conn.close()
    
def is_video_document(message_media_document):
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeVideo):
                return True
    return False

def is_round_video_document(message_media_document):
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeRoundVideo):
                return True
    return False


def is_audio_document(message_media_document):
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeAudio):
                return True
    return False
    
def is_sticker_document(message_media_document):
    if isinstance(message_media_document, MessageMediaDocument):
        for attribute in message_media_document.document.attributes:
            if isinstance(attribute, DocumentAttributeSticker):
                return True
    return False
    
def get_message_type(message: Message):
    if message.media and is_video_document(message.media):
        return "Video"
    elif message.media and is_round_video_document(message.media):
        return "Round video"
    elif message.media and is_audio_document(message.media):
        return "Audio"
    elif message.media and is_sticker_document(message.media):
        return "Sticker"
    elif type(message.media).__name__ == 'MessageMediaPhoto':
        return "Photo"
    elif message.text:
        return "Text"
    else:
        return "Other"

def save_message_statistics(message: Message):
    conn = sqlite3.connect('telegram_stats_db.db')
    cursor = conn.cursor()

    # Получаем информацию о сообщении
    user_id = message.from_id.user_id if message.from_id else None
    chat_id = message.chat_id
    message_type = get_message_type(message)

    # Обновляем статистику
    cursor.execute('''
        UPDATE statistics 
        SET count = COALESCE(count, 0) + 1 
        WHERE user_id = ? AND message_type = ?
    ''', (user_id, message_type))

    # Если ни одной записи не было обновлено, значит, создаем новую
    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO statistics (user_id, message_type, count)
            VALUES (?, ?, 1)
        ''', (user_id, message_type))
    
 
    #print(f"Added message type: {message_type} for user ID: {user_id}")
    
    conn.commit()
    conn.close()
    Dostalivse2003,
    