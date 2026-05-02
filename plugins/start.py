from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL
from plugins.utils.markup import Buttons # Import from your new folder

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    user = message.from_user
    
    # --- LOG CHANNEL NOTIFICATION ---
    # This sends an update to your log channel every time someone starts the bot
    await client.send_message(
        LOG_CHANNEL,
        f"👤 <b>New User Started Bot</b>\n\n"
        f"‣ <b>Name:</b> {user.first_name}\n"
        f"‣ <b>ID:</b> <code>{user.id}</code>\n"
        f"‣ <b>Username:</b> @{user.username if user.username else 'No Username'}"
    )

    # --- FILE RETRIEVAL LOGIC ---
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].replace("file_", ""))
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=LOG_CHANNEL,
                message_id=file_id
            )
        except Exception:
            await message.reply_text("❌ <b>File not found or deleted from server.</b>")
        return

    # --- MAIN START MENU ---
    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=f"👋 <b>Hey {user.first_name}!</b>\n\n"
                "I can convert your files into high-speed direct links.\n\n"
                "• <b>Direct Download Link</b>\n"
                "• <b>Fast Streaming Support</b>\n\n"
                "Just send any file now 👇",
        reply_markup=Buttons.START_BUTTONS, # Using the button from your utils folder
        parse_mode=enums.ParseMode.HTML
    )
    
