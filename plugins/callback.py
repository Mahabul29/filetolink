import time
from pyrogram import Client
from pyrogram.types import CallbackQuery
from plugins.utils.markup import Buttons

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "about":
        # Calculate Ping
        start_time = time.time()
        # Simulated check (Pyrogram latency is usually handled via message timing)
        end_time = time.time()
        ping = round((end_time - start_time) * 1000, 2)

        about_text = (
            "‣ <b>ᴍʏ ɴᴀᴍᴇ :</b> ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ\n"
            "‣ <b>ʟɪʙʀᴀʀʏ :</b> ᴘʏʀᴏɢʀᴀᴍ\n"
            "‣ <b>ᴅᴀᴛᴀʙᴀsᴇ :</b> ᴍᴏɴɢᴏᴅʙ\n"
            "‣ <b>ʟᴀɴɢᴜᴀɢᴇ :</b> ᴘʏᴛʜᴏɴ 𝟹\n"
            "‣ <b>ʙᴏᴛ sᴇʀᴠᴇʀ :</b> ᴋᴏʏᴇʙ\n"
            "‣ <b>ᴘɪɴɢ :</b> <code>{ping} ms</code>\n"
            "‣ <b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ :</b> <a href='https://t.me/Mahabul201'>Moon</a>"
        )
        
        await query.message.edit_caption(
            caption=about_text,
            reply_markup=Buttons.BACK_BUTTON
        )

    elif query.data == "help":
        help_text = (
            "<b>📖 Bot Help Menu</b>\n\n"
            "1. Send me any File, Video, or Audio.\n"
            "2. I will store it in my Database.\n"
            "3. You will get a permanent Download Link.\n\n"
            "<i>Note: Direct links are high-speed!</i>"
        )
        await query.message.edit_caption(
            caption=help_text,
            reply_markup=Buttons.BACK_BUTTON
        )

    elif query.data == "back":
        # Returns user to the main start screen
        await query.message.edit_caption(
            caption=f"<b>👋 Hey {query.from_user.first_name}!</b>\n\n"
                    "Send any file or media to get:\n\n"
                    "• <b>Direct Download Link</b>\n\n"
                    "Just send the file now 👇",
            reply_markup=Buttons.START_BUTTONS
        )
      
