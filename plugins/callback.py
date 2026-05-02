from pyrogram import Client
from pyrogram.types import CallbackQuery
from plugins.utils.markup import Buttons

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "about":
        # Updated to match the "About" style in your screenshot
        about_text = (
            "▶ <b>MY NAME :</b> SHORTLINK BOT\n"
            "▶ <b>LIBRARY :</b> PYROGRAM\n"
            "▶ <b>DATABASE :</b> MONGODB\n"
            "▶ <b>LANGUAGE :</b> PYTHON 3\n"
            "▶ <b>BOT SERVER :</b> KOYEB\n"
            "▶ <b>CREATED BY :</b> Moon"
        )
        await query.message.edit_caption(
            caption=about_text,
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )

    elif data == "help":
        # Modified Help Menu
        help_text = (
            "<b>💡 How to Use Me?</b>\n\n"
            "1️⃣ Add me to your channel or send a file here.\n"
            "2️⃣ I will provide a high-speed download link.\n"
            "3️⃣ Use the 'Bot' button to share the link with others!\n\n"
            "<i>Everything is automated and instant.</i>"
        )
        await query.message.edit_caption(
            caption=help_text,
            reply_markup=Buttons.BACK_CLOSE_BUTTONS
        )

    elif data == "back_to_start":
        # Returns to the original Start Message
        start_caption = (
            "👋 <b>Hey Moon!</b>\n\n"
            "I can convert your files into high-speed direct links.\n\n"
            "• Direct Download Link\n"
            "• Fast Streaming Support\n\n"
            "Just send any file now 👇"
        )
        await query.message.edit_caption(
            caption=start_caption,
            reply_markup=Buttons.START_BUTTONS
        )

    elif data == "close":
        # Deletes the message completely
        await query.message.delete()
