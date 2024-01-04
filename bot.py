# from telegram.ext import Updater, CommandHandler

# TOKEN = '6419038563:AAH6uLuDCXGzflLBejIr7v6CRvyLynsDQ6M'

# def get_chat_id(update, context):
#     chat_id = update.message.chat_id

#     with open('chat_id.txt', 'w') as file:
#         file.write(str(chat_id))

#     update.message.reply_text(f"The Chat ID is: {chat_id}")

# def main():
#     updater = Updater(TOKEN, use_context=True)
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler("getid", get_chat_id))

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()


from telegram.ext import Updater, CommandHandler

# Dictionary to store message statistics
message_stats = {
    'total_messages': 0,
    'text_messages': 0,
    'photo_messages': 0,
    'video_messages': 0,
    # Add more types if needed
}

TOKEN = '6419038563:AAH6uLuDCXGzflLBejIr7v6CRvyLynsDQ6M'
# Function to update message statistics
def update_stats(update, context):
    message = update.message
    message_stats['total_messages'] += 1

    # Update message type statistics
    if message.text:
        message_stats['text_messages'] += 1
    elif message.photo:
        message_stats['photo_messages'] += 1
    elif message.video:
        message_stats['video_messages'] += 1
    # Add more conditions for different message types

    # You can extend this to capture more message types (audio, document, etc.)

# Function to display message statistics
def show_stats(update, context):
    stats_text = f"Total Messages: {message_stats['total_messages']}\n" \
                 f"Text Messages: {message_stats['text_messages']}\n" \
                 f"Photo Messages: {message_stats['photo_messages']}\n" \
                 f"Video Messages: {message_stats['video_messages']}\n"
    # Add more stats as needed

    update.message.reply_text(stats_text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("updatestats", update_stats))
    dp.add_handler(CommandHandler("showstats", show_stats))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()