import os
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL

# FIXED: Use __name__ so the logger knows which file is reporting errors
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
                    # FIXED: Added int() wrapper to LOG_CHANNEL just in case
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=int(LOG_CHANNEL),
                        message_id=file_id
                    )
                    return  
                
                except Exception as e:
                    logger.error(f"File copy error: {e}")
                    await message.reply_text(
                        "<b>❌ File not found or has been deleted from our server.</b>", 
                        parse_mode=enums.ParseMode.HTML
                    )
                    return

        # 2. FALLBACK: Normal Welcome Message
        user_name = message.from_user.first_name if message.from_user else "User"
        
        # Added a button to make it look professional
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Mahabul29")
        ]])

        welcome_text = (
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 <b>How to use:</b>\n"
            "Just send or forward any file/video to me, and I will "
            "generate a high-speed download link for you instantly!\n\n"
            "⚡ <i>Powered by JavaGoat</i>"
        )
        
        await message.reply_text(
            text=welcome_text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=markup,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        # This will now correctly show up in your Koyeb logs
        logger.error(f"CRITICAL ERROR in start.py: {e}", exc_info=True)
        await message.reply_text("❌ Something went wrong! Please try again later.")
        
