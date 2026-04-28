from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

def make_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    stream_link = f"https://{clean_host}/dl/{file_id}"
    return stream_link, InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴅ", url=stream_link)]
    ])

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # 1. Identify the media type and extract info
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown_File")
        # Convert bytes to MB for readability
        file_size = f"{media.file_size / (1024 * 1024):.2f} MB"

        # 2. Store the file
        copied_msg = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        stream_link, markup = make_buttons(copied_msg.id)
        
        # 3. Reply with File Info
        await message.reply_text(
            f"<b>ғɪʟᴇ sᴛᴏʀᴇ</b>\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
            f"<b>sɪᴢᴇ:</b> <code>{file_size}</code>\n\n"
            f"ᴅᴏᴡɴʟᴏᴅ: <code>{stream_link}</code>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        
