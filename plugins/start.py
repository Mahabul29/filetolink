
from pyrogram import Client, filters
from pyrogram.types import Message

# This function will handle the /start command
async def start_cmd(client: Client, message: Message):
    try:
        # Get the user's name safely
        user_name = message.from_user.first_name if message.from_user else "User"
        
        # Define the message text
        welcome_text = (
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 <b>How to use:</b>\n"
            "Just send or forward any file/video to me, and I will "
            "generate a high-speed download link for you instantly!"
        )
        
        # Send the reply
        await message.reply_text(
            text=welcome_text,
            parse_mode="html",
            disable_web_page_preview=True
        )
        
    except Exception as e:
        # If there is an error, this prints it to your Koyeb logs
        print(f"CRITICAL ERROR in start.py: {e}")
        
