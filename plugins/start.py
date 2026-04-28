import os
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    try:
        # 1. PRIORITY: Check if this is a "Deep Link" (e.g., /start file_428)
        if len(message.command) > 1:
            data = message.command[1]
            
            if data.startswith("file_"):
                try:
                    # Extract the message ID (file_428 -> 428)
                    file_id = int(data.replace("file_", ""))
                    
                    # Send the actual file from your Log Channel to the User
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=int(LOG_CHANNEL),
                        message_id=file_id
                    )
                    return  # EXIT HERE so the welcome message is NOT sent
                
                except ValueError:
                    await message.reply_text("<b>❌ Invalid File Link.</b>", parse_mode=enums.ParseMode.HTML)
                    return

        # 2. FALLBACK: Normal Welcome Message
        user_name = message.from_user.first_name if message.from_user else "User"
        welcome_text = (
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 <b>How to use:</b>\n"
            "Just send or forward any file/video to me, and I will "
            "generate a high-speed download link for you instantly!"
        )
        
        await message.reply_text(
            text=welcome_text,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR in start.py: {e}")
        await message.reply_text("Something went wrong! Please try again later.")
        
