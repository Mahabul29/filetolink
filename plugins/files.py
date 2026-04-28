import logging
from pyrogram import Client, filters
from config import LOG_CHANNEL, FQDN

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        msg = await message.copy(chat_id=int(LOG_CHANNEL))
        
        file_id = msg.id
        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        download_link = f"https://{clean_host}/dl/{file_id}"

        await message.reply_text(
            f"<b>✅ Your Download Link:</b>\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode="html"
        )
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
