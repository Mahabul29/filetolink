import time
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from config import LOG_CHANNEL, ADMINS
from plugins.utils.markup import Buttons
from plugins.utils.database import db 

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user = message.from_user
    await db.add_user(user.id)
    
    # --- DEEP LINK LOGIC ---
    if len(message.command) > 1:
        data = message.command[1]
        if data.startswith("file_"):
            try:
                file_id = int(data.split("_")[1])
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=LOG_CHANNEL,
                    message_id=file_id
                )
                return 
            except Exception as e:
                await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")
                return

    # --- WELCOME MESSAGE ---
    caption = (
        f"👋 <b>ʜᴇʏ {user.first_name}!!</b>\n\n"
        "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴀꜱ ᴡᴇʟʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴏʀ!!\n\n"
        "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ!!\n\n"
        "<b>ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ 👇</b>"
    )

    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=caption,
        reply_markup=Buttons.START_BUTTONS
    )

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users_cmd(client, message):
    count = await db.total_users_count()
    await message.reply_text(f"📊 <b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ:</b> <code>{count}</code>")

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        return await message.reply_text("<b>❌ ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ!!</b>")
    
    broadcast_msg
    
