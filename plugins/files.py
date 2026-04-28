from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

def make_buttons(file_id):
    # Cleans the host and creates the download URL
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    stream_link = f"https://{clean_host}/dl/{file_id}"
    
    # Returns the URL and the Inline Button
    return stream_link, InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴅ", url=stream_link)]
    ])

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # 1. Identify the media type and extract metadata
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown_File")
        
        # 2. Format file size to 2 decimal places in MB
        file_size = f"{media.file_size / (1024 * 1024):.2f} MB"

        # 3. Store the file in the log channel
        copied_msg = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        # 4. Generate the link and button markup
        stream_link, markup = make_buttons(copied_msg.id)
        
        # 5. Reply to user with clickable link
        await message.reply_text(
            f"<b>ғɪʟᴇ sᴛᴏʀᴇ</b>\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
            f"<b>sɪᴢᴇ:</b> <code>{file_size}</code>\n\n"
            f"<b>ᴅᴏᴡɴʟᴏᴅ:</b> <a href='{stream_link}'>{stream_link}</a>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        
