import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL  # Using the combined channel

# FIXED: Standard logger initialization
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    try:
        # 1. HANDLE DEEP LINKS (/start file_123)
        if len(message.command) > 1:
            data = message.command[1]
            
            if data.startswith("file_"):
                try:
                    # Extract ID: "file_428" -> 428
                    file_id = int(data.replace("file_", ""))
                    
                    # Copy the message from your combined LOG_CHANNEL to the user
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=int(LOG_CHANNEL),
                        message_id=file_id
                    )
                    return # Exit so we don't send the welcome text too
                
                except Exception as e:
                    logger.error(f"Deep link error: {e}")
                    await message.reply_text(
                        "<b>❌ File not found.</b>\nIt may have been deleted from the storage channel.",
                        parse_mode=enums.ParseMode.HTML
                    )
                    return

        # 2. NORMAL WELCOME MESSAGE
        user_name = message.from_user.first_name if message.from_user else "User"
        
        # Adding buttons to make it look professional
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📢 Updates", url="https://t.me/JavaGoat"),
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Mahabul29")
            ]
        ])

        welcome_text = (
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 <b>How to use:</b>\n"
            "Send or forward any file to me, and I will generate "
            "a high-speed download link for you instantly!\n\n"
            "⚡ <i>Powered by JavaGoat Streaming</i>"
        )
        
        await message.reply_text(
            text=welcome_text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        logger.error(f"Error in start.py: {e}", exc_info=True)
        await message.reply_text("❌ Something went wrong! Please try again later.")
        
