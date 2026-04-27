from pyrogram import Client, filters, enums
from pyrogram.types import Message

async def start_cmd(client: Client, message: Message):
    try:
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
            parse_mode=enums.ParseMode.HTML,   # ← This is the correct way in Pyrogram v2
            disable_web_page_preview=True
        )
        
    except Exception as e:
        print(f"CRITICAL ERROR in start.py: {e}")
        try:
            await message.reply_text("Something went wrong! Please try again.")
        except:
            pass
