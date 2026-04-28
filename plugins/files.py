import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

logger = logging.getLogger(__name__)


# ====================== PRIVATE CHAT FILE HANDLER ======================
@Client.on_message(
    filters.private &
    (filters.document | filters.video | filters.audio)
)
async def file_handler(client: Client, message: Message):
    try:
        # Copy file to LOG_CHANNEL/BIN_CHANNEL to store it
        copied_msg = await message.copy(chat_id=int(LOG_CHANNEL))
        file_id = copied_msg.id

        clean_host = FQDN.strip().rstrip("/")
        stream_link = f"https://{clean_host}/dl/{file_id}"
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
            [InlineKeyboardButton("🤖 Get via Bot", url=bot_link)]
        ])

        await message.reply_text(
            f"<b>✅ Your Download Link is Ready!</b>\n\n"
            f"🔗 <code>{stream_link}</code>\n\n"
            f"⚡ <i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"File handler error: {e}", exc_info=True)
        await message.reply_text("❌ Sorry, something went wrong while generating the link.")


# ====================== CHANNEL POST HANDLER ======================
@Client.on_message(
    filters.channel &
    (filters.document | filters.video | filters.audio)
)
async def channel_file_handler(client: Client, message: Message):
    try:
        file_id = message.id
        clean_host = FQDN.strip().rstrip("/")
        stream_link = f"https://{clean_host}/dl/{file_id}"
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🚀 Fast Download", url=stream_link),
                InlineKeyboardButton("🤖 Get via Bot", url=bot_link)
            ]
        ])

        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"Channel handler error: {e}", exc_info=True)
