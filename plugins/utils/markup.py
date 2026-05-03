from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help") # Must match cb_handler
        ],
        [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")]
    ])

    BACK_CLOSE_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_start"),
            InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")
        ]
    ])
    
    @staticmethod
    def file_links(dl, bot):
        return InlineKeyboardMarkup([[
            InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=dl),
            InlineKeyboardButton("ʙᴏᴛ", url=bot)
        ]])
        
