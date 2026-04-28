import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

logger = logging.getLogger(__name__)

@Client.on_message(
    (filters.private | filters.channel) & 
    (filters.document | filters.video | filters.audio)
)
async def file_handler(client, message):
    try:
        msg = await message.copy(chat_id=int(LOG_CHANNEL))
        
        file_id = msg.id
        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        download_link = f"https://{clean_host}/dl/{file_id}"

        file_obj = message.document or message.video or message.audio
        file_name = getattr(file_obj, 'file_name', None) or "Unknown"
        file_size = f"{round(file_obj.file_size / (1024 * 1024), 2)} MB"

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Server 1 🔺", url=download_link),
                InlineKeyboardButton("Server 2 🔺", url=download_link)
            ]
        ])

        await client.send_document(
            chat_id=message.chat.id,
            document=file_obj.file_id,
            caption=(
                f"📑 <b>FILE DETAILS FOUND</b>\n\n"
                f"📝 <b>Name:</b> <code>{file_name}</code>\n"
                f"⚖️ <b>Size:</b> <code>{file_size}</code>\n\n"
                f"🔗 <i>Your direct download links are generated below:</i>"
            ),
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ Error: {e}")
