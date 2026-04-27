from pyrogram import Client, filters

async def start_cmd(client, message):
    try:
        user_name = message.from_user.first_name or "User"
        
        # Simple, solid text response
        text = (
            f"👋 <b>Hey {user_name},</b>\n\n"
            f"🤖 I am online and ready! Just send me any <b>file or video</b> 📤 "
            f"and I will instantly convert it into a 🔗 <b>direct download link</b> ⚡.\n\n"
            f"✅ <b>High-speed links</b>\n"
            f"✅ <b>No ads</b>"
        )
        
        await message.reply_text(
            text=text,
            parse_mode="html",
            disable_web_page_preview=True
        )
        
    except Exception as e:
        # This will show in your Koyeb logs if something goes wrong
        print(f"Error in start_cmd: {e}")
        
