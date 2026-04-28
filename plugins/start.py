import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    # 1. Handle Link Retrieval
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].replace("file_", ""))
            
            # Use int() to prevent 'Peer ID Invalid' errors
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=int(LOG_CHANNEL),
                message_id=file_id
            )
            return
        except Exception as e:
            logger.error(f"Retrieve Error: {e}")
            await message.reply_text("<b>❌ File not found or deleted.</b>", parse_mode=enums.ParseMode.HTML)
            return

    # 2. Handle Normal Welcome
    user_name = message.from_user.first_name if message.from_user else "User"
    buttons = InlineKeyboardMarkup([[
        InlineKeyboardButton("📢 Updates", url="https://t.me/JavaGoat"),
        InlineKeyboardButton("👨‍💻 Dev", url="https://t.me/Mahabul29")
    ]])

    await message.reply_text(
        f"<b>👋 Hello {user_name}!</b>\n\nSend me any file and I will give you a link.",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=buttons
    )
    
