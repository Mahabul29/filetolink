from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from config import BASE_URL, LOG_CHANNEL

logger = logging.getLogger(__name__)

async def file_handler(client, message):
    try:
        # We use LOG_CHANNEL for everything now
        if not LOG_CHANNEL:
            return await message.reply_text("❌ Log Channel not configured.")

        # Forward file to your Log Channel (this acts as storage)
        msg = await message.forward(LOG_CHANNEL)
        file_id = msg.id

        download_link = f"{BASE_URL}/dl/{file_id}"

        media = message.document or message.video or message.audio or message.photo
        file_name = getattr(media, "file_name", "File")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2) if file_size else "?"

        reply_text = f"""<b>📂 File:</b> <code>{file_name}</code>
<b>📦 Size:</b> <code>{size_mb} MB</code>

<b>🔗 Your Link Is Ready!</b>"""

        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton("⚡ Download", url=download_link)
        ]])

        await message.reply_text(reply_text, reply_markup=buttons, parse_mode="html")

        # Send the "Power Log" to the same channel
        await client.send_message(
            LOG_CHANNEL,
            f"📥 <b>New File Stored & Logged</b>\n\n"
            f"👤 <b>User:</b> {message.from_user.mention}\n"
            f"📂 <b>File:</b> <code>{file_name}</code>\n"
            f"📦 <b>Size:</b> {size_mb} MB\n"
            f"🔗 <b>Link:</b> {download_link}"
        )

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.reply_text("❌ Error processing file. Make sure I am Admin in the Log Channel.")
        
