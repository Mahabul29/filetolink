import os
from pyrogram import filters
import logging

logger = logging.getLogger(__name__)

# Updated text: Removed "smooth streaming"
START_TXT = """<b>👋 Hey {},</b>

🤖 I'm <b>{}</b> 🚀 — just send me any <b>file or video</b> 📤 and I'll instantly convert it into a 🔗 <b>direct download link</b> ⚡.

<b>Features:</b>
✅ High-speed direct links
✅ Works in Google Chrome
✅ No ads or shorteners

➕ Add me as an <b>admin</b> to your channel 📢 and I'll create download links for every post automatically!"""

START_PIC = os.environ.get("START_PIC", "")

async def start_cmd(client, message):
    logger.info(f"[START] User {message.from_user.id} sent /start")
    user_name = message.from_user.first_name or "User"
    
    try:
        bot_info = await client.get_me()
        bot_name = bot_info.first_name or "FileBot"
    except Exception:
        bot_name = "FileBot"

    if START_PHOTO:
        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=START_TXT.format(user_name, bot_name),
                parse_mode="html"
            )
            return
        except Exception as e:
            logger.error(f"Photo failed: {e}")

    await message.reply_text(
        START_TXT.format(user_name, bot_name),
        disable_web_page_preview=True,
        parse_mode="html"
    )
    
