import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

logger = logging.getLogger(__name__)

# Filter: Private/Channel files, but IGNORES anything starting with "/" (commands)
@Client.on_message(
    (filters.private | filters.channel) & 
    (filters.document | filters.video | filters.audio) & 
    ~filters.regex(r"^/") 
)
async def file_handler(client, message):
    try:
        # 1. Store the file in your Log Channel
        target_chat = int(LOG_CHANNEL)
        msg = await message.copy(chat_id=target_chat)
        
        # 2. Extract metadata
        file_obj = message.document or message.video or message.audio
        file_name = file_obj.file_name
        file_size = f"{round(file_obj.file_size / (1024 * 1024), 2)} MB"
        
        # 3. Generate links
        file_id = msg.id
        clean_host = FQDN.strip("/")
        download_link = f"https://{clean_host}/dl/{file_id}"

        # 4. Buttons
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Server 1 🔺", url=download_link),
                InlineKeyboardButton("Server 2 🔺", url=download_link)
            ]
        ])

        # 5. Response 1: File Information Card
        info_text = (
            f"📑 <b>FILE DETAILS FOUND</b>\n\n"
            f"📝 <b>Name:</b> <code>{file_name}</code>\n"
            f"⚖️ <b>Size:</b> <code>{file_size}</code>\n\n"
            f"🔗 <i>Your direct download links are generated below:</i>"
        )
        
        await message.reply_text(
            text=info_text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )

        # 6. Response 2: Direct file return (No forwarding needed)
        await message.reply_document(
            document=file_obj.file_id,
            caption=f"✅ <b>File Received:</b> <code>{file_name}</code>",
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"Error in file_handler: {e}")
        
