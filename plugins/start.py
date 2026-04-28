from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].replace("file_", ""))
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=LOG_CHANNEL,
                message_id=file_id
            )
        except Exception as e:
            await message.reply_text(f"❌ File not found: {e}")
        return

    await message.reply_photo(
    photo="https://img.uhdpaper.com/wallpaper/genshin-impact-furina-game-art-16@1@m-pc-4k.jpg",
    caption=f"<b>👋 Hey {message.from_user.first_name}!</b>\n\n"
            "Send any file or media to get:\n\n"
            "• <b>Direct Download Link</b>\n\n"
            "Just send the file now 👇",
    parse_mode=enums.ParseMode.HTML
    )
