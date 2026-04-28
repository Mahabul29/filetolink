import logging
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, FQDN

# Fixed: Use __name__ to correctly initialize the logger
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        # Forward or copy the message to the Log Channel to get a persistent Message ID
        msg = await message.copy(chat_id=int(LOG_CHANNEL))
        
        # The ID of the message in the LOG_CHANNEL is used for the download link
        file_id = msg.id
        
        # Clean the FQDN to ensure there are no double slashes or protocol conflicts
        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        download_link = f"https://{clean_host}/dl/{file_id}"

        # Reply to the user with the generated link
        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        # This will now work correctly since 'logger' is defined
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ Error: Something went wrong while generating the link.")
        
