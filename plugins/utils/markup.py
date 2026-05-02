from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # ... (Keep START_BUTTONS and BACK_BUTTON the same)

    @staticmethod
    def file_links(download_link, bot_link):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link),
                InlineKeyboardButton("ʙᴏᴛ", url=bot_link)
            ]
        ])
        
