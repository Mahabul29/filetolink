from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # The Main Start Menu
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")
        ]
    ])

    # The Back button used in About/Help pages
    BACK_BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back")]
    ])
    
