from pyrogram import Client, filters
from plugins.utils.markup import Buttons

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    help_text = (
        "📖 <b>ʜᴇʟᴘ ᴍᴇɴᴜ</b>\n\n"
        "<b>ᴄᴏᴍᴍᴀɴᴅꜱ:</b>\n"
        "• /start — ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
        "• /help — ꜱʜᴏᴡ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ\n\n"
        "<b>ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:</b>\n"
        "1️⃣ ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ, ᴠɪᴅᴇᴏ, ᴏʀ ᴀᴜᴅɪᴏ\n"
        "2️⃣ ɪ'ʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ\n"
        "3️⃣ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ!\n\n"
        "⚡ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ꜰɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ</i>"
    )
    await message.reply_text(
        text=help_text,
        reply_markup=Buttons.BACK_CLOSE_BUTTONS
    )
    
