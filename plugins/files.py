import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

# Use __name__ to avoid the NameError
logger = logging.getLogger(__name__)

# 1. START COMMAND HANDLER
@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await message.reply_text(
        f"<b>Hello {message.from_user.mention}!</b>\n\n"
        f"I am a File to Link Generator bot. Send me any file and I will give you a high-speed download link.",
        parse_mode=enums.ParseMode.HTML
    )

# 2. FILE HANDLER (Generates the Link)
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def file_handler(client, message):
    try:
        # Copy the file to the log channel
        msg = await message.copy(chat_id=int(LOG_CHANNEL))
        
        file_id = msg.id
        clean_host = FQDN.strip("/").replace("https://", "").replace("http://", "")
        download_link = f"https://{clean_host}/dl/{file_id}"

        # Create a button for the link
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀 Fast Download", url=download_link)]]
        )

        await message.reply_text(
            f"<b>✅ Your Download Link is Ready:</b>\n\n"
            f"🔗 <code>{download_link}</code>\n\n"
            f"<i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"File Storage Error: {e}")
        await message.reply_text(f"❌ Error: {e}")
        
