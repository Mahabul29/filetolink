import time
from pyrogram import Client, filters
from plugins.utils.markup import Buttons
from plugins.utils.database import db 
from config import LOG_CHANNEL, ADMINS

# We define the caption once here so it's easy to change
START_TEXT = (
    "👋 <b>ʜᴇʏ ᴍᴏᴏɴ!!</b>\n\n"
    "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴀꜱ ᴡᴇʟʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴏʀ!!\n\n"
    "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ!!\n\n"
    "<b>ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ 👇</b>"
)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user = message.from_user
    await db.add_user(user.id)
    
    # Deep Link Logic (Fixes the BOT link)
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].split("_")[1])
            await client.copy_message(message.chat.id, LOG_CHANNEL, file_id)
            return
        except: pass

    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=START_TEXT,
        reply_markup=Buttons.START_BUTTONS
    )

@Client.on_message(filters.command("ping") & filters.private)
async def ping_cmd(client, message):
    start = time.time()
    msg = await message.reply_text("🚀")
    await msg.edit_text(f"🏓 <b>ᴘᴏɴɢ!!</b>\n<code>{round((time.time() - start) * 1000)}ᴍꜱ</code>")
    
