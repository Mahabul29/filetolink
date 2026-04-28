import logging
from pyrogram import Client, filters, enums  # Added enums here
from config import LOG_CHANNEL, FQDN

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        # Convert to int to ensure it's a valid Peer ID
        target_chat = int(LOG_CHANNEL)

        # Copy file to storage channel
        msg = await message.copy(chat_id=target_chat)
        
        # Build the link
        file_id = msg.id
        clean_host = FQDN.strip("/")
        download_link = f"https://{clean_host}/dl/{file_id}"

        # FIX: Use enums.ParseMode.HTML instead of "html"
        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        # Use the same fix for the error message reply
        await message.reply_text(
            f"❌ <b>Error:</b> <code>{e}</code>", 
            parse_mode=enums.ParseMode.HTML
        )
        
