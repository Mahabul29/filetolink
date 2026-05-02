# plugins/utils/markup.py
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    START_BUTTONS = InlineKeyboardMarkup([
        [
            # Ensure these strings are exactly "about" and "help"
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")
        ]
    ])
    
