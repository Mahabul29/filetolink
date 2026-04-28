import logging
from pyrogram import Client, filters
from config import LOG_CHANNEL, FQDN  # Using FQDN to match your variables

logger = logging.getLogger(__name__)

# THIS DECORATOR IS THE TRIGGER:
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))
async def file_handler(client, message):
    try:
        # 1. Copy file to your storage channel
        msg = await message.copy(chat_id=LOG_CHANNEL)
        
        # 2. Build the link
        # We ensure https:// is present and use FQDN from your config
        file_id = msg.id
        
        # Clean the FQDN to prevent double slashes
        clean_fqdn = FQDN.strip('/')
        download_link = f"https://{clean_fqdn}/dl/{file_id}"

        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode="html"
        )
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
        
