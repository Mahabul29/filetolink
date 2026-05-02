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

    # row 1: [Download, Bot]
    @staticmethod
    def file_links(download_link, bot_link):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link),
                InlineKeyboardButton("ʙᴏᴛ", url=bot_link)
            ]
        ])

    # row 1: [Back, Close] - SIDE BY SIDE
    BACK_CLOSE_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Bᴀᴄᴋ", callback_data="back"),
            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")
        ]
    ])
    
