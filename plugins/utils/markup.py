from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Buttons:
    # Side-by-side: [Button1, Button2] inside ONE bracket
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mahabul201")
        ]
    ])

    # Side-by-side for the Download links
    @staticmethod
    def file_links(download_link, bot_link):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link),
                InlineKeyboardButton("ʙᴏᴛ", url=bot_link)
            ]
        ])

    BACK_BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back")]
    ])
    
