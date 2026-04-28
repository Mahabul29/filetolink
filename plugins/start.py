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

    await message.reply_text(
        f"<b>👋 Hello {message.from_user.first_name}!</b>\n\nSend me a file to get a link.",
        parse_mode=enums.ParseMode.HTML
    )
