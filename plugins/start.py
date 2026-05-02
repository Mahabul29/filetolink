from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL, ADMIN_ID # Ensure ADMIN_ID is in your config
# Assuming you have a simple database helper, if not, I'll provide one below
# from database import add_user, get_total_users 

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    # 1. Track the user (Registration)
    # await add_user(message.from_user.id) 

    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].replace("file_", ""))
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=LOG_CHANNEL,
                message_id=file_id
            )
        except Exception as e:
            await message.reply_text(f"❌ File not found or has been deleted.")
        return

    # Normal Start Message
    await message.reply_photo(
        photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
        caption=f"<b>👋 Hey {message.from_user.first_name}!</b>\n\n"
                "I am a File Store Bot. Send me any file and I will store it "
                "and give you a permanent link!\n\n"
                "• <b>Direct Download Link</b>\n"
                "• <b>Fast Streaming</b>\n\n"
                "Just send a file to begin 👇",
        parse_mode=enums.ParseMode.HTML
    )

# 2. Add a Stats Command for the Admin
@Client.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_handler(client: Client, message: Message):
    # total = await get_total_users()
    total = "Database not connected" # Placeholder
    await message.reply_text(f"📊 <b>Bot Statistics</b>\n\nTotal Users: <code>{total}</code>")
    
