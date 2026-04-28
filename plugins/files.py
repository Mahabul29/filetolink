import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client: Client, message: Message):
    try:
        # Use LOG_CHANNEL as the storage
        chat_id = int(LOG_CHANNEL)

        # Copy message to storage channel
        copied_msg = await client.copy_message(
            chat_id=chat_id,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        file_id = copied_msg.id
        
        # Clean FQDN
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        
        # Links
        stream_link = f"https://{clean_host}/dl/{file_id}"
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
            [InlineKeyboardButton("🤖 Get via Bot", url=bot_link)]
        ])

        await message.reply_text(
            f"<b>✅ Your Download Link is Ready!</b>\n\n"
            f"🔗 <code>{bot_link}</code>\n\n"
            f"⚡ <i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error in file_handler: {e}")
        await message.reply_text(f"❌ Error: {e}")
