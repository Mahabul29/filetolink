from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BIN_CHANNEL

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply_text(
        "👋 **Hello! Send me any file to get a link.**",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Dev", url="https://t.me/Mahabul29")
        ]])
    )
    
