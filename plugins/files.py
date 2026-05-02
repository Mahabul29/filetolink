from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

def make_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
    stream_link = f"https://{clean_host}/dl/{file_id}"
    
    # Buttons placed in a single list [button1, button2] appear side-by-side
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link),
            InlineKeyboardButton("ʙᴏᴛ", url=bot_link)
        ]
    ])
    return bot_link, stream_link, markup

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # Forward the file to the log channel to get a persistent message ID
        copied_msg = await message.copy(chat_id=LOG_CHANNEL)

        # Generate links and the side-by-side buttons
        bot_link, stream_link, markup = make_buttons(copied_msg.id)

        # Efficiently extract file metadata
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown_File")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2)

        await message.reply_text(
            f"<b>✅ File Stored Successfully!</b>\n\n"
            f"📁 <b>Name:</b> <code>{file_name}</code>\n"
            f"📦 <b>Size:</b> <code>{size_mb} MB</code>\n\n"
            f"🔗 <b>Bot Link:</b>\n<code>{bot_link}</code>\n\n"
            f"⚡ <b>Stream Link:</b>\n<code>{stream_link}</code>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
        
