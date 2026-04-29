from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

def make_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
    stream_link = f"https://{clean_host}/dl/{file_id}"
    return bot_link, stream_link, InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link)],   # Fixed spelling
        [InlineKeyboardButton("ɢᴇᴛ ᴠɪᴀ ʙᴏᴛ", url=bot_link)]
    ])

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        copied_msg = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )

        bot_link, stream_link, markup = make_buttons(copied_msg.id)

        # Get file information
        file_name = message.document.file_name if message.document else \
                    message.video.file_name if message.video else \
                    message.audio.file_name if message.audio else "Unknown_File"

        file_size = message.document.file_size if message.document else \
                    message.video.file_size if message.video else \
                    message.audio.file_size if message.audio else 0

        size_mb = round(file_size / (1024 * 1024), 2)

        await message.reply_text(
            f"<b>✅ File Stored!</b>\n\n"
            f"📁 <b>File Name:</b> <code>{file_name}</code>\n"
            f"📦 <b>File Size:</b> <code>{size_mb} MB</code>\n\n"
            f"🔗 <b>Bot Link:</b>\n<code>{bot_link}</code>\n\n"
            f"⚡ <b>Stream Link:</b>\n<code>{stream_link}</code>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
