
import logging
from pyrogram import Client, filters
from config import LOG_CHANNEL, FQDN

logger = logging.getLogger(__name__)

# This line triggers the code when you send a file
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        # 1. Copy the file to your storage channel
        msg = await message.copy(chat_id=LOG_CHANNEL)
        
        # 2. Generate the link
        # We use FQDN and the message ID from the log channel
        file_id = msg.id
        
        # Clean FQDN just in case there's a typo in your variables
        clean_host = FQDN.strip("/")
        download_link = f"https://{clean_host}/dl/{file_id}"

        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode="html"
        )
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
        
