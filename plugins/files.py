import logging
from html import escape
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Ensure these variables are correctly set in your config.py
from config import LOG_CHANNEL, FQDN, API_ID, API_HASH, BOT_TOKEN

# Setup logging to see errors in the console
logging.basicConfig(level=logging.ERROR)

app = Client(
    "file_store_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def make_buttons(message_id):
    """
    Constructs the download link and the inline button.
    Uses the message_id from the LOG_CHANNEL.
    """
    # Clean FQDN: remove protocols and trailing slashes to avoid double slashes in URL
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    stream_link = f"https://{clean_host}/dl/{message_id}"
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link)]
    ])
    return markup

@app.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # 1. Identify the media and extract metadata
        media = message.document or message.video or message.audio
        
        # Escape HTML special characters to prevent "Message_Empty" or parsing errors
        raw_name = getattr(media, "file_name", "Unknown_File") or "Unknown_File"
        file_name = escape(raw_name)

        # 2. Format File Size (KB, MB, or GB)
        size_bytes = media.file_size
        if size_bytes < 1024 * 1024:
            file_size = f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            file_size = f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            file_size = f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

        # 3. Copy file to LOG_CHANNEL
        # We use copy_message to get a new message ID in the storage channel
        copied_msg = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        # 4. Generate the UI components
        # Note: Your website must be configured to fetch files using this Message ID
        markup = make_buttons(copied_msg.id)
        
        # 5. Send the final response to the user
        await message.reply_text(
            f"<b>ғɪʟᴇ sᴛᴏʀᴇ</b>\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
            f"<b>sɪᴢᴇ:</b> <code>{file_size}</code>\n\n",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        logging.error(f"Error in handler: {e}")
        # Optional: alert the user an error occurred
        # await message.reply_text("❌ Failed to process file.")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
    
