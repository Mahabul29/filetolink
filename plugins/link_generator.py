from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BIN_CHANNEL, FQDN

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client, message):
    msg = await message.reply_text("⏳ <b>Processing...</b>")
    try:
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)

        download_link = f"https://{FQDN}/dl/{copied_msg.id}"
        stream_link = f"https://{FQDN}/watch/{copied_msg.id}"

        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⬇ Download", url=download_link),
                InlineKeyboardButton("▶ Stream", url=stream_link)
            ]
        ])

        await msg.edit_text(
            f"✅ <b>File Stored Successfully!</b>\n\n"
            f"📂 <b>Name:</b> <code>{file_name}</code>\n"
            f"📦 <b>Size:</b> <code>{size_mb} MB</code>\n\n"
            f"🔗 <b>Links Generated!</b>",
            reply_markup=keyboard
        )

    except Exception as e:
        await msg.edit_text(f"❌ <b>Error:</b> <code>{e}</code>")
