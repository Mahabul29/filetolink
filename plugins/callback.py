from pyrogram import Client
from plugins.utils.markup import Buttons

@Client.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    
    START_TEXT = (
        "👋 <b>ʜᴇʏ ᴍᴏᴏɴ!!</b>\n\n"
        "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴀꜱ ᴡᴇʟʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴏʀ!!\n\n"
        "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ!!\n\n"
        "<b>ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ 👇</b>"
    )

    if data == "about":
        await query.message.edit_caption(
            caption="▶ <b>ᴍʏ ɴᴀᴍᴇ :</b> ꜰɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ\n▶ <b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ :</b> ᴍᴏᴏɴ",
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )
    
    elif data == "help":
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
        await query.message.edit_caption(
            caption=help_text,
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )

    elif data == "back_to_start":
        await query.message.edit_caption(
            caption=START_TEXT,
            reply_markup=Buttons.START_BUTTONS
        )

    elif data == "close":
        await query.message.delete()
        
