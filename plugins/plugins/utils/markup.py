from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # Main Menu
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/Moon")
        ]
    ])

    # About Page Back Button
    BACK_BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back")]
    ])
  
