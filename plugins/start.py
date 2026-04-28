import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL # Make sure LOG_CHANNEL is imported

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    try:
        # 1. Check if this is a "Deep Link" from your website button
        if len(message.command) > 1:
            data = message.command[1]
            if data.startswith("file_"):
                # Extract the message ID from the link (e.g., file_428 -> 428)
                file_id = int(data.replace("file_", ""))
                
                # Send the file from your Log Channel to the User
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=int(LOG_CHANNEL),
                    message_id=file_id
                )
                return # Stop here so we don't send the welcome message

        # 2. Normal Welcome Message
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
        print(f"CRITICAL ERROR in start.py: {e}")
        try:
            await message.reply_text("Something went wrong! Please try again.")
        except:
            pass
            
