from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

def make_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
    stream_link = f"https://{clean_host}/dl/{file_id}"
    return bot_link, stream_link, InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴅ", url=stream_link)],
        [InlineKeyboardButton("ɢᴇᴛt ᴠɪᴀ ʙᴏᴛ", url=bot_link)]
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
        await message.reply_text(
            f"<b>✅ File Stored!</b>\n\n"
            f"🔗 Bot Link: <code>{bot_link}</code>\n"
            f"⚡ Stream: <code>{stream_link}</code>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
