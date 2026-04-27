import os
from pyrogram import filters
import logging

logger = logging.getLogger(__name__)

START_TXT = """<b>👋 Hey {},</b>

🤖 I'm <b>{}</b> 🚀 — just send me any <b>file or video</b> 📤 and I'll instantly convert it into 🔗 <b>direct download</b> & 🎬 <b>smooth streaming links</b> ⚡ with fast processing and reliable access.

➕ You can also add me as an <b>admin</b> to your channel 📢 and I'll automatically create download & stream links with ready-to-use buttons for every media you post ✨ making sharing easy and seamless."""

START_PHOTO = os.environ.get("START_PIC", "")

async def start_cmd(client, message):
    logger.info(f"[START] User {message.from_user.id} ({message.from_user.first_name}) sent /start")

    user_name = message.from_user.first_name or "User"
    
    try:
        bot_info = await client.get_me()
        bot_name = bot_info.first_name or "FileBot"
    except Exception as e:
        logger.error(f"[START] Failed to get bot info: {e}")
        bot_name = "FileBot"

    try:
        if START_PHOTO:
            await message.reply_photo(
                photo=START_PHOTO,
                caption=START_TXT.format(user_name, bot_name),
                parse_mode="html"
            )
        else:
            await message.reply_text(
                START_TXT.format(user_name, bot_name),
                disable_web_page_preview=True,
                parse_mode="html"
            )
        logger.info(f"[START] Reply sent successfully to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"[START] Failed to send message: {e}")
        await message.reply_text("👋 Hello! Send me any file to get a direct download link.")
