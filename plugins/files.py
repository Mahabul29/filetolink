from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BASE_URL, BIN_CHANNEL, LOG_CHANNEL

async def file_handler(client, message):
    try:
        # Forward file to storage
        msg = await message.forward(BIN_CHANNEL)
        file_id = msg.id # This is the unique ID for the link

        download_link = f"{BASE_URL}/dl/{file_id}"

        # Get file metadata
        media = message.document or message.video or message.audio or message.photo
        file_name = getattr(media, "file_name", "File")
        
        reply_text = f"<b>📂 File:</b> <code>{file_name}</code>\n\n<b>🔗 Link Ready!</b>"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Download", url=download_link)]
        ])

        await message.reply_text(reply_text, reply_markup=buttons, parse_mode="html")

    except Exception as e:
        print(f"Error generating link: {e}")
        
