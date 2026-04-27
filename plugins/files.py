import logging
from pyrogram import Client, filters
from config import LOG_CHANNEL, BASE_URL

logger = logging.getLogger(__name__)

async def file_handler(client, message):
    try:
        # Copy file to your storage channel
        msg = await message.copy(chat_id=LOG_CHANNEL)
        
        # Link generation using the message ID from the storage channel
        file_id = msg.id
        download_link = f"{BASE_URL}/dl/{file_id}"

        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode="html"
        )
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
        
