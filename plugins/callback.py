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
    
    elif data == "help":
        help_text = (
            "📖 <b>ʜᴇʟᴘ ᴍᴇɴᴜ</b>\n\n"
            "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ, ᴠɪᴅᴇᴏ, ᴏʀ ᴀᴜᴅɪᴏ.\n"
            "ɪ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ ᴀɴᴅ ᴀ ʙᴏᴛ ʟɪɴᴋ ᴛᴏ ꜱʜᴀʀᴇ!"
        )
        await query.message.edit_caption(
            caption=help_text,
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )

    elif data == "back_to_start":
        # MATCHED: This now matches the start_cmd caption exactly
        start_caption = (
            "👋 <b>ʜᴇʏ ᴍᴏᴏɴ!!</b>\n\n"
            "ɪ'ᴍ ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇꜱ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴀꜱ ᴡᴇʟʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴏʀ!!\n\n"
            "ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ!!\n\n"
            "<b>ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ 👇</b>"
        )
        await query.message.edit_caption(
            caption=start_caption,
            reply_markup=Buttons.START_BUTTONS
        )

    elif data == "close":
        await query.message.delete()
        
