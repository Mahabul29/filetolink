from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BIN_CHANNEL, FQDN

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client, message):
    try:
        # Store file in BIN_CHANNEL
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)
        
        # Setup Links
        download_link = f"https://{FQDN}/dl/{copied_msg.id}"
        stream_link = f"https://{FQDN}/watch/{copied_msg.id}"

        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)

        # EXACT TEXT AND NO EMOJIS AS REQUESTED
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("DOWNLOAD", url=download_link),
                InlineKeyboardButton("STREAM", url=stream_link)
            ]
        ])

        await message.reply_text(
            f"✅ <b>FILE STORED SUCCESSFULLY!!</b>\n\n"
            f"📂 <b>NAME:</b> <code>{file_name}</code>\n"
            f"📦 <b>SIZE:</b> <code>{size_mb} MB</code>\n\n"
            f"🔗 <b>LINKS GENERATED!</b>",
            reply_markup=keyboard
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        
