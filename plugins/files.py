import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FQDN, LOG_CHANNEL

# Use __name__ to avoid the NameError
logger = logging.getLogger(__name__)

# Change the filter to listen to Channels
@Client.on_message(filters.channel & (filters.document | filters.video | filters.audio))
async def channel_file_handler(client, message):
    try:
        # We process the file by copying it to the Log Channel first.
        # This keeps our download DB organized.
        log_msg = await message.copy(chat_id=int(LOG_CHANNEL))
        
        file_id = log_msg.id
        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        # Standard download link
        download_link = f"https://{clean_host}/dl/{file_id}"
        # Alternative link (server 2) can go here if needed
        # alternate_link = f"https://server2.{clean_host}/dl/{file_id}" 

        # Create the buttons (as seen in your screenshot)
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Server 1 🔺", url=download_link),
                    InlineKeyboardButton("Server 2 🔺", url=download_link) # Pointing to the same link for now
                ]
            ]
        )

        # Edit the original post in the source channel to add the buttons
        # We maintain the original caption if it exists.
        await message.edit_caption(
            caption=message.caption or "",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"Channel File Processing Error: {e}")
        # Note: In a channel, you generally do NOT want to reply with the error
        # message, as it will break the channel feed. We only log it.

