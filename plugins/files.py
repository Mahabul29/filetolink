from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from config import BASE_URL, BIN_CHANNEL, LOG_CHANNEL

logger = logging.getLogger(__name__)

async def file_handler(client, message):
    try:
        msg = await message.forward(BIN_CHANNEL)
        file_id = msg.id

        download_link = f"{BASE_URL}/dl/{file_id}"

        media = message.document or message.video or message.audio or message.photo
        file_name = getattr(media, "file_name", "File")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2) if file_size else "?"

        reply_text = f"""<b>📂 File:</b> <code>{file_name}</code>
<b>📦 Size:</b> <code>{size_mb} MB</code>

<b>🔗 Your Link Is Ready!</b>"""

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚡ Download", url=download_link)
            ]
        ])

        await message.reply_text(
            reply_text,
            reply_markup=buttons,
            parse_mode="html"
        )

        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"📥 New file uploaded\n"
                f"👤 User: {message.from_user.mention}\n"
                f"📂 File: {file_name}\n"
                f"📦 Size: {size_mb} MB\n"
                f"🔗 Link: {download_link}"
            )

    except Exception as e:
        logger.error(f"[FILE] Error: {e}")
        await message.reply_text("❌ Failed to generate link. Please try again.")
