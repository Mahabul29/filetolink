import logging
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, FQDN

# Fixed: __name__ is the standard way to initialize the logger
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        # Copy the file to your log/storage channel
        msg = await message.copy(chat_id=int(LOG_CHANNEL))
        
        # Use the message ID from the log channel for the link
        file_id = msg.id
        
        # Clean the host URL to prevent formatting errors
        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        download_link = f"https://{clean_host}/dl/{file_id}"

        # Send the success message back to the user
        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        # Log the error and notify the user
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ Error: {e}")
        
