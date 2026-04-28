import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

logger = logging.getLogger(__name__)

# ── Private chat: file → generate link ──────────────────────────────
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        msg = await message.copy(chat_id=int(LOG_CHANNEL))
        file_id = msg.id

        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        stream_link = f"https://{clean_host}/dl/{file_id}"
        bot_link    = f"https://t.me/{File_To_Link2_Bot}?start=file_{file_id}"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
            [InlineKeyboardButton("🤖 Get via Bot",   url=bot_link)]
        ])

        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{stream_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"File handler error: {e}")
        await message.reply_text(f"❌ Error: {e}")


# ── Channel post: auto-add Download button ───────────────────────────
@Client.on_message(filters.channel & (filters.document | filters.video | filters.audio))
async def channel_file_handler(client, message):
    try:
        file_id = message.id

        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        stream_link = f"https://{clean_host}/dl/{file_id}"
        bot_link    = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🚀 Fast Download", url=stream_link),
                InlineKeyboardButton("🤖 Get via Bot",   url=bot_link)
            ]
        ])

        # Edit the channel post to add the buttons
        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"Channel handler error: {e}")
