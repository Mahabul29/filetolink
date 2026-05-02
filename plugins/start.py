import time
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL, ADMINS # Ensure ADMINS list is in config.py
from plugins.utils.markup import Buttons

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user = message.from_user
    
    # 1. Log Channel Notification
    await client.send_message(
        LOG_CHANNEL,
        f"👤 <b>New User:</b> {user.first_name}\n"
        f"‣ <b>ID:</b> <code>{user.id}</code>"
    )

    # 2. File Retrieval Logic
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].replace("file_", ""))
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=LOG_CHANNEL,
                message_id=file_id
            )
        except Exception:
            await message.reply_text("❌ <b>File not found or deleted.</b>")
        return

    # 3. Main Start Menu
    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=f"👋 <b>Hey {user.first_name}!</b>\n\n"
                "I can convert your files into high-speed direct links.\n\n"
                "Just send any file now 👇",
        reply_markup=Buttons.START_BUTTONS
    )

# --- NEW COMMANDS ---

@Client.on_message(filters.command("ping") & filters.private)
async def ping_cmd(client, message):
    start = time.time()
    msg = await message.reply_text("🚀 Pinging...")
    end = time.time()
    await msg.edit_text(f"<b>🏓 Pong!</b>\n<code>{round((end - start) * 1000)}ms</code>")

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users_cmd(client, message):
    # This requires a database implementation to show real numbers
    await message.reply_text("<b>👥 Total Members:</b> <code>Fetching from Database...</code>")

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to a message to broadcast.")
    await message.reply_text("🚀 <b>Broadcast Started...</b>")
    
