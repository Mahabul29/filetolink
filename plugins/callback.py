from pyrogram import Client
from plugins.utils.markup import Buttons

@Client.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    
    if data == "about":
        await query.message.edit_caption(
            caption="▶ <b>ᴍʏ ɴᴀᴍᴇ :</b> ꜰɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ\n▶ <b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ :</b> ᴍᴏᴏɴ",
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )
    elif data == "back_to_start":
        start_caption = (
            "👋 <b>ʜᴇʏ!!</b>\n\n"
            "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ!!\n\n"
            "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ ɴᴏᴡ 👇"
        )
        await query.message.edit_caption(
            caption=start_caption,
            reply_markup=Buttons.START_BUTTONS
        )
    elif data == "close":
        await query.message.delete()
        
