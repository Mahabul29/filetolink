from pyrogram import Client
from pyrogram.types import CallbackQuery
from plugins.utils.markup import Buttons

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "about":
        about_text = (
            "▶ <b>ᴍʏ ɴᴀᴍᴇ :</b> ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ\n"
            "▶ <b>ʟɪʙʀᴀʀʏ :</b> ᴘʏʀᴏɢʀᴀᴍ\n"
            "▶ <b>ᴅᴀᴛᴀʙᴀꜱᴇ :</b> ᴍᴏɴɢᴏᴅʙ\n"
            "▶ <b>ʟᴀɴɢᴜᴀɢᴇ :</b> ᴘʏᴛʜᴏɴ 3\n"
            "▶ <b>ʙᴏᴛ ꜱᴇʀᴠᴇʀ :</b> ᴋᴏʏᴇʙ\n"
            "▶ <b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ :</b> ᴍᴏᴏɴ"
        )
        await query.message.edit_caption(
            caption=about_text,
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )

    elif data == "help":
        help_text = (
            "<b>💡 ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴍᴇ?</b>\n\n"
            "1️⃣ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴏʀ ꜱᴇɴᴅ ᴀ ꜰɪʟᴇ ʜᴇʀᴇ.\n"
            "2️⃣ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴀ ʜɪɢʜ-ꜱᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ.\n"
            "3️⃣ ᴜꜱᴇ ᴛʜᴇ 'ʙᴏᴛ' ʙᴜᴛᴛᴏɴ ᴛᴏ ꜱʜᴀʀᴇ ʟɪɴᴋꜱ!\n\n"
            "<i>ᴇᴠᴇʀʏᴛʜɪɴɢ ɪꜱ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ᴀɴᴅ ɪɴꜱᴛᴀɴᴛ.</i>"
        )
        await query.message.edit_caption(
            caption=help_text,
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )

    elif data == "back_to_start":
        start_caption = (
            "👋 <b>ʜᴇʏ!!</b>\n\n"
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
        
