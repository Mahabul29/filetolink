import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    # Handle the file retrieval
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].replace("file_", ""))
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=int(LOG_CHANNEL),
                message_id=file_id
            )
            return
        except Exception as e:
            logger.error(f"Retrieve Error: {e}")
            await message.reply_text("❌ File not found in our storage.")
            return

    # Default welcome message
    await message.reply_text(
        f"<b>👋 Hello {message.from_user.first_name}!</b>\n\n"
        "I am your <b>File to Link Bot</b>. Send me any file to get started!",
        parse_mode=enums.ParseMode.HTML
    )
    
