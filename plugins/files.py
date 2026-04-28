from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from html import escape
from config import LOG_CHANNEL, FQDN, BOT_USERNAME, API_ID, API_HASH, BOT_TOKEN

app = Client(
    "file_store_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def make_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    stream_link = f"https://{clean_host}/dl/{file_id}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link)]
    ])

@app.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # 1. Extract media and handle missing filenames
        media = message.document or message.video or message.audio
        raw_name = getattr(media, "file_name", "Unknown_File") or "Unknown_File"
        file_name = escape(raw_name)

        # 2. Convert bytes to MB
        file_size = f"{media.file_size / (1024 * 1024):.2f} MB"

        # 3. Store the file in Log Channel
        copied_msg = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        markup = make_buttons(copied_msg.id)
        
        # 4. Final Reply
        await message.reply_text(
            f"<b>ғɪʟᴇ sᴛᴏʀᴇ</b>\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
            f"<b>sɪᴢᴇ:</b> <code>{file_size}</code>\n\n",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run()
    
