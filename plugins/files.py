import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

logger = logging.getLogger(__name__)

# Updated filter: Added filters.chat() or filters.channel to work in channels
@Client.on_message((filters.private | filters.channel) & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        # 1. Store the file in your Log Channel
        target_chat = int(LOG_CHANNEL)
        msg = await message.copy(chat_id=target_chat)
        
        # 2. Extract file details for a professional look
        file_obj = message.document or message.video or message.audio
        file_name = file_obj.file_name
        file_size = f"{round(file_obj.file_size / (1024 * 1024), 2)} MB"
        
        # 3. Generate your website link
        file_id = msg.id
        clean_host = FQDN.strip("/")
        download_link = f"https://{clean_host}/dl/{file_id}"

        # 4. Create the Inline Buttons (Server 1 and Server 2 style)
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Server 1 🔺", url=download_link),
                InlineKeyboardButton("Server 2 🔺", url=download_link)
            ]
        ])

        # 5. Send the professional response
        await message.reply_text(
            f"📂 <b>FILE NAME :</b> <code>{file_name}</code>\n"
            f"📦 <b>FILE SIZE :</b> <code>{file_size}</code>\n\n"
            f"🚀 <b>Your high-speed links are ready!</b>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )
        
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(
            f"❌ <b>Error:</b> <code>{e}</code>", 
            parse_mode=enums.ParseMode.HTML
        )
        
