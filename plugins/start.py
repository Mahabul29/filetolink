import os
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    try:
        # 1. Check for Deep Links (e.g., t.me/bot?start=file_511)
        if len(message.command) > 1:
            data = message.command[1]
            
            if data.startswith("file_"):
                try:
                    file_id = int(data.replace("file_", ""))
                    
                    # Better Practice: Use copy_message but add a caption check
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=int(LOG_CHANNEL),
                        message_id=file_id
                    )
                    return 
                
                except Exception as e:
                    logger.error(f"Deep link error: {e}")
                    await message.reply_text("<b>❌ File not found or has been deleted.</b>", parse_mode=enums.ParseMode.HTML)
                    return

        # 2. Normal Welcome Message
        user_name = message.from_user.first_name if message.from_user else "User"
        welcome_text = (
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 <b>How to use:</b>\n"
            "Just send or forward any file/video to me, and I will "
            "generate a high-speed download link for you instantly!\n\n"
            "<i>Powered by JavaGoat Streaming</i>"
        )
        
        # Added a photo for the start command (as you mentioned wanting a photo)
        # Replace 'https://...' with your actual image URL
        await message.reply_photo(
            photo="https://graph.org/file/your-image-id.jpg", 
            caption=welcome_text,
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR in start.py: {e}")
        # Only show the error to the user if you absolutely have to
        await message.reply_text("Something went wrong! Please try again later.")
        
