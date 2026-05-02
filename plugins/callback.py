from pyrogram import Client
from pyrogram.types import CallbackQuery
from plugins.utils.markup import Buttons

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "about":
        await query.message.edit_caption(
            caption="‣ <b>ᴍʏ ɴᴀᴍᴇ :</b> ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ\n‣ <b>ʟɪʙʀᴀʀʏ :</b> ᴘʏʀᴏɢʀᴀᴍ\n‣ <b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ :</b> Moon",
            reply_markup=Buttons.BACK_BUTTON
        )
    elif query.data == "help":
        await query.message.edit_caption(
            caption="<b>ʜᴇʟᴘ ᴍᴇɴᴜ:</b>\nJust send me any file or media, and I will generate a direct download link for you instantly!",
            reply_markup=Buttons.BACK_BUTTON
        )
    elif query.data == "back":
        await query.message.edit_caption(
            caption="👋 <b>Hey!</b>\n\nSend any file or media to get a direct download link.",
            reply_markup=Buttons.START_BUTTONS
        )
        
