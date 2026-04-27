import os
from pyrogram import Client, filters

# I have updated this to the direct 4K image link for Furina
START_PIC = "https://images.uhdpaper.com/wallpapers/genshin-impact-furina-game-4k-wallpaper-pc-phone-3840x2160-161m.jpg" 

START_TXT = """<b>👋 Hey {},</b>

🤖 I'm <b>{}</b> 🚀 — just send me any <b>file or video</b> 📤 and I'll instantly convert it into a 🔗 <b>direct download link</b> ⚡.

<b>Features:</b>
✅ High-speed direct links
✅ Works in Google Chrome
✅ No ads or shorteners"""

async def start_cmd(client, message):
    user_name = message.from_user.first_name or "User"
    
    try:
        bot_info = await client.get_me()
        bot_name = bot_info.first_name or "FileBot"
    except Exception:
        bot_name = "FileBot"

    # This sends the Furina image you liked
    if START_PIC:
        try:
            await message.reply_photo(
                photo=START_PIC,
                caption=START_TXT.format(user_name, bot_name),
                parse_mode="html"
            )
            return 
        except Exception:
            pass 

    # Fallback if the image link ever breaks
    await message.reply_text(
        START_TXT.format(user_name, bot_name),
        disable_web_page_preview=True,
        parse_mode="html"
    )
    
