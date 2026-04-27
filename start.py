from pyrogram import filters
import logging

logger = logging.getLogger(__name__)

# Import Script
from Script import script

async def start_cmd(client, message):
    logger.info(f"[START] User {message.from_user.id} ({message.from_user.first_name}) sent /start")
    
    user_name = message.from_user.first_name or "User"
    
    try:
        await message.reply_text(
            script.START_MSG.format(user_name),
            disable_web_page_preview=True
        )
        logger.info(f"[START] Reply sent successfully to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"[START] Failed to send message: {e}")
        await message.reply_text("👋 Hello! Send me any file to get a direct download link.")
