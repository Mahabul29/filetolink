from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import LOG_CHANNEL, BOT_USERNAME
# from database import add_user # Uncomment if using DB

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    # --- LOG CHANNEL NOTIFICATION ---
    user = message.from_user
    # is_new = await add_user(user.id) # Check if user is new in DB
    # if is_new: 
    await client.send_message(
        LOG_CHANNEL,
        f"👤 <b>New User Started Bot</b>\n\n"
        f"‣ <b>Name:</b> {user.first_name}\n"
        f"‣ <b>ID:</b> <code>{user.id}</code>\n"
        f"‣ <b>Username:</b> @{user.username}"
    )

    if len(message.command) > 1 and message.command[1].startswith("file_"):
        # ... (keep your existing file copying logic here)
        return

    # --- MAIN START MENU ---
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠʟᴏᴘᴇʀ", url="https://t.me/Mahabul201") # Change to your link
        ]
    ])

    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=f"👋 <b>Hey {user.first_name}!</b>\n\n"
                "Send any file or media to get:\n"
                "• <b>Direct Download Link</b>\n\n"
                "Just send the file now 👇",
        reply_markup=buttons
    )
    
