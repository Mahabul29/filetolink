from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # row 1: [About, Help] | row 2: [Developer]
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")
        ]
    ])

    # NEW: This fixes the 'no attribute file_links' error
    @staticmethod
    def file_links(download_link, bot_link):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link),
                InlineKeyboardButton("ʙᴏᴛ", url=bot_link)
            ]
        ])

    # Side-by-Side: [Back, Close]
    BACK_CLOSE_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/Mahabul201")
        ],
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_start"),
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ])
    
