import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)


@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client: Client, message: Message):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Updates", url="https://t.me/JavaGoat")],
        [InlineKeyboardButton("Developer", url="https://t.me/Mahabul29")]
    ])

    await message.reply_text(
        "<b>📖 Help Menu</b>\n\n"
        "<b>Commands:</b>\n"
        "• /start — Start the bot\n"
        "• /help — Show this help message\n\n"
        "<b>How to use:</b>\n"
        "1️⃣ Send any file, video, or audio to me\n"
        "2️⃣ I'll instantly give you a direct download link\n"
        "3️⃣ Share the link with anyone!\n\n"
        "⚡ <i>Powered by JavaGoat Streaming</i>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=markup,
        disable_web_page_preview=True
    )
