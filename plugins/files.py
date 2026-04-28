import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

logger = logging.getLogger(__name__)

# --- PRIVATE CHAT HANDLER ---
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_file_handler(client: Client, message: Message):
    try:
        # Store file in the storage channel
        copied_msg = await client.copy_message(
            chat_id=int(LOG_CHANNEL),
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        file_id = copied_msg.id
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
        stream_link = f"https://{clean_host}/dl/{file_id}"

        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
            [InlineKeyboardButton("🤖 Get via Bot", url=bot_link)]
        ])

        await message.reply_text(
            f"<b>✅ Your Download Link is Ready!</b>\n\n🔗 <code>{bot_link}</code>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Private Handler Error: {e}")
        await message.reply_text(f"❌ Error: <code>{e}</code>")

# --- CHANNEL POST HANDLER ---
@Client.on_message(filters.channel & (filters.document | filters.video | filters.audio))
async def channel_file_handler(client: Client, message: Message):
    # Skip if message is already in storage to avoid loops
    if message.chat.id == int(LOG_CHANNEL):
        return

    try:
        file_id = message.id
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
        stream_link = f"https://{clean_host}/dl/{file_id}"

        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
            [InlineKeyboardButton("🤖 Get via Bot", url=bot_link)]
        ])

        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Channel Edit Error: {e}")
        
