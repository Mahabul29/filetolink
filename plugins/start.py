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

# --- ADMIN COMMANDS ---

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users_cmd(client, message):
    count = await db.total_users_count()
    await message.reply_text(f"📊 <b>ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ:</b> <code>{count}</code>")

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        return await message.reply_text("<b>❌ ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ!!</b>")
    
    broadcast_msg = message.reply_to_message
    status_msg = await message.reply_text("🚀 <b>ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴛᴀʀᴛᴇᴅ...</b>")
    
    users = await db.get_all_users()
    success = 0
    failed = 0
    
    async for user in users:
        try:
            await broadcast_msg.copy(chat_id=user["_id"])
            success += 1
            await asyncio.sleep(0.1) # Prevent Flood
        except (UserIsBlocked, InputUserDeactivated):
            failed += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id=user["_id"])
            success += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ <b>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!!</b>\n\n"
        f"👤 <b>ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ:</b> <code>{success + failed}</code>\n"
        f"🎉 <b>ꜱᴜᴄᴄᴇꜱꜱ:</b> <code>{success}</code>\n"
        f"❌ <b>ꜰᴀɪʟᴇᴅ:</b> <code>{failed}</code>"
    )

@Client.on_message(filters.command("ping") & filters.private)
async def ping_cmd(client, message):
    start = time.time()
    msg = await message.reply_text("🚀")
    end = time.time()
    await msg.edit_text(f"🏓 <b>ᴘᴏɴɢ!!</b>\n<code>{round((end - start) * 1000)}ᴍꜱ</code>")
    
