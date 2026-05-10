import os
import sys
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from plugins.utils.markup import Buttons
from plugins.utils.database import db 
from config import LOG_CHANNEL, ADMINS

# This captures the exact time the bot starts
START_TIME = time.time()

START_TEXT = (
    "👋 <b>ʜᴇʏ ᴍᴏᴏɴ!!</b>\n\n"
    "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴀꜱ ᴡᴇʟʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴏʀ!!\n\n"
    "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ!!\n\n"
    "<b>ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ 👇</b>"
)

# --- USER COMMANDS ---

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    # Add user to database
    await db.add_user(message.from_user.id)
    
    # Handle Deep Links
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
        "• /help — ꜱʜᴏᴡ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ\n"
        "• /data — ᴄʜᴇᴄᴋ ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ\n\n"
        "<b>ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:</b>\n"
        "1️⃣ ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ, ᴠɪᴅᴇᴏ, ᴏʀ ᴀᴜᴅɪᴏ\n"
        "2️⃣ ɪ'ʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ\n"
        "3️⃣ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ!\n\n"
        "⚡ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ꜰɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ</i>"
    )
    await message.reply_text(help_text, reply_markup=Buttons.BACK_CLOSE_BUTTONS)

@Client.on_message(filters.command("ping") & filters.private)
async def ping_cmd(client, message):
    start = time.time()
    msg = await message.reply_text("🚀")
    await msg.edit_text(f"🏓 <b>ᴘᴏɴɢ!!</b>\n<code>{round((time.time() - start) * 1000)}ᴍꜱ</code>")

@Client.on_message(filters.command("data") & filters.private)
async def data_cmd(client, message):
    """Shows how many days/hours the bot has been running"""
    now = time.time()
    delta_obj = now - START_TIME
    
    # Calculate time units
    days = int(delta_obj // (24 * 3600))
    hours = int((delta_obj % (24 * 3600)) // 3600)
    minutes = int((delta_obj % 3600) // 60)
    seconds = int(delta_obj % 60)

    # Fetch total users from DB
    count = await db.total_users_count()

    stats_text = (
        "📊 <b>ʙᴏᴛ ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ ᴅᴀᴛᴀ</b>\n\n"
        f"👤 <b>ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ:</b> <code>{count}</code>\n"
        f"🕒 <b>ᴜᴘᴛɪᴍᴇ:</b> <code>{days}ᴅ {hours}ʜ {minutes}ᴍ {seconds}ꜱ</code>\n\n"
        "🛰 <b>ꜱᴛᴀᴛᴜꜱ:</b> <code>ꜱʏꜱᴛᴇᴍ ᴏɴʟɪɴᴇ</code>"
    )
    await message.reply_text(stats_text)

# --- ADMIN COMMANDS ---

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users_cmd(client, message):
    count = await db.total_users_count()
    await message.reply_text(f"📊 <b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ:</b> <code>{count}</code>")

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_cmd(client, message):
    """Restarts the bot process"""
    msg = await message.reply_text("🔄 **ᴘʀᴏᴄᴇꜱꜱɪɴɢ...**")
    await msg.edit_text("✅ **ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛɪɴɢ...**\n*ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴀ ꜰᴇᴡ ꜱᴇᴄᴏɴᴅꜱ.*")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ **ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ.**")

    all_users = await db.get_all_users() 
    broadcast_msg = message.reply_to_message
    sts_msg = await message.reply_text("📣 **ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴛᴀʀᴛᴇᴅ...**")
    
    success, failed, done = 0, 0, 0
    total = await db.total_users_count()

    async for user in all_users:
        try:
            user_id = user['_id'] 
            await broadcast_msg.copy(chat_id=int(user_id))
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id=int(user_id))
            success += 1
        except Exception:
            failed += 1
        
        done += 1
        if done % 20 == 0:
            await sts_msg.edit(
                f"📣 **ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ:**\n\n"
                f"👤 **ᴛᴏᴛᴀʟ:** `{total}`\n"
                f"✅ **ꜱᴜᴄᴄᴇꜱꜱ:** `{success}`\n"
                f"❌ **ꜰᴀɪʟᴇᴅ:** `{failed}`"
            )

    await sts_msg.edit(
        f"📢 **ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!!**\n\n"
        f"✅ **ꜱᴜᴄᴄᴇꜱꜱ:** `{success}`\n"
        f"❌ **ꜰᴀɪʟᴇᴅ:** `{failed}`"
    )
    
