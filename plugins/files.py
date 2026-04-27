from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BASE_URL, BIN_CHANNEL

async def file_handler(client, message):
    try:
        # Forward the file to the merged Bin/Log channel
        msg = await message.forward(BIN_CHANNEL)
        file_id = msg.id

        download_link = f"{BASE_URL}/dl/{file_id}"

        media = message.document or message.video or message.audio or message.photo
        file_name = getattr(media, "file_name", "File")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2) if file_size else "?"

        reply_text = f"<b>📂 File:</b> <code>{file_name}</code>\n<b>📦 Size:</b> <code>{size_mb} MB</code>\n\n<b>🔗 Your Link Is Ready!</b>"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Download", url=download_link)]
        ])

        # Reply to the user
        await message.reply_text(reply_text, reply_markup=buttons, parse_mode="html")

        # Log the activity in the SAME channel
        await client.send_message(
            BIN_CHANNEL,
            f"📥 <b>File Processed</b>\n"
            f"👤 <b>User:</b> {message.from_user.mention}\n"
            f"📂 <b>Name:</b> {file_name}\n"
            f"🔗 <b>Link:</b> {download_link}"
        )

    except Exception as e:
        print(f"Error: {e}")
        
