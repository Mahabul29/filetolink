from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # Main Start Menu Buttons
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")
        ]
    ])

    # Side-by-Side Download/Bot Buttons (Emojis Removed)
    @staticmethod
    def file_links(download_link, bot_link):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link),
                InlineKeyboardButton("ʙᴏᴛ", url=bot_link)
            ]
        ])

    # Side-by-Side Back and Close (Emojis Removed)
    BACK_CLOSE_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Mahabul201")
        ],
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_start"),
            InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")
        ]
    ])
    
