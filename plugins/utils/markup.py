from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # Main Start Menu
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")
        ]
    ])

    # About/Help Menu (Back and Close side-by-side)
    BACK_CLOSE_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Mahabul201")
        ],
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_start"),
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ])
    
