from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client: Client, message: Message):
    await message.reply_text(
        "<b>📌 How to Use This Bot:</b>\n\n"
        "1. Send any file (video, document, audio)\n"
        "2. Bot will automatically generate download link\n\n"
        "<b>Commands:</b>\n"
        "/start - Start the bot\n"
        "/help - Show this message\n\n"
        "<i>Powered by JavaGoat Streaming</i>",
        parse_mode="html"
    )
