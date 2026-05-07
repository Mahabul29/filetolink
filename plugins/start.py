import os
import sys
import time
from pyrogram import Client, filters
from plugins.utils.markup import Buttons
from plugins.utils.database import db 
from config import LOG_CHANNEL, ADMINS

START_TEXT = (
    "👋 <b>ʜᴇʏ ᴍᴏᴏɴ!!</b>\n\n"
    "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴀꜱ ᴡᴇʟʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴏʀ!!\n\n"
    "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ!!\n\n"
    "<b>ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ 👇</b>"
)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    # Save user to DB immediately
    await db.add_user(message.from_user.id)
    
    # Check for Deep Links (Bot Link click)
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].split("_")[1])
            await client.copy_message(message.chat.id, LOG_CHANNEL, file_id)
            return
        except Exception as e:
            print(f"Error in deep link: {e}")
            return

    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=START_TEXT,
        reply_markup=Buttons.START_BUTTONS
    )

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    help_text = (
        "📖 <b>ʜᴇʟᴘ ᴍᴇɴᴜ</b>\n\n"
        "<b>ᴄᴏᴍᴍᴀɴᴅꜱ:</b>\n"
        "• /start — ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
        "• /help — ꜱʜᴏᴡ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ\n\n"
        "<b>ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:</b>\n"
        "1️⃣ ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ, ᴠɪᴅᴇᴏ, ᴏʀ ᴀᴜᴅɪᴏ\n"
        "2️⃣ ɪ'ʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ\n"
        "3️⃣ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ!\n\n"
        "⚡ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ꜰɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ</i>"
    )
    await message.reply_text(help_text, reply_markup=Buttons.BACK_CLOSE_BUTTONS)

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users_cmd(client, message):
    count = await db.total_users_count()
    await message.reply_text(f"📊 <b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ:</b> <code>{count}</code>")

@Client.on_message(filters.command("ping") & filters.private)
async def ping_cmd(client, message):
    start = time.time()
    msg = await message.reply_text("🚀")
    await msg.edit_text(f"🏓 <b>ᴘᴏɴɢ!!</b>\n<code>{round((time.time() - start) * 1000)}ᴍꜱ</code>")

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_cmd(client, message):
    """Restart the bot process"""
    msg = await message.reply_text("🔄 **ᴘʀᴏᴄᴇꜱꜱɪɴɢ...**")
    await msg.edit_text("✅ **ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛɪɴɢ...**\n*ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴀ ꜰᴇᴡ ꜱᴇᴄᴏɴᴅꜱ.*")
    
    # This replaces the current running process with a fresh one
    os.execl(sys.executable, sys.executable, *sys.argv)
    
