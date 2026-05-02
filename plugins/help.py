@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client: Client, message: Message):
    # This keeps your custom buttons side-by-side
    from plugins.utils.markup import Buttons
    
    help_text = (
        "📖 <b>ʜᴇʟᴘ ᴍᴇɴᴜ</b>\n\n"
        "<b>ᴄᴏᴍᴍᴀɴᴅꜱ:</b>\n"
        "• /start — ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n"
        "• /help — ꜱʜᴏᴡ ᴛʜɪꜱ ʜᴇʟᴘ ᴍᴇꜱꜱᴀɢᴇ\n\n"
        "<b>ʜᴏᴡ ᴛᴏ ᴜꜱᴇ:</b>\n"
        "1️⃣ ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ, ᴠɪᴅᴇᴏ, ᴏʀ ᴀᴜᴅɪᴏ ᴛᴏ ᴍᴇ\n"
        "2️⃣ ɪ'ʟʟ ɪɴꜱᴛᴀɴᴛʟʏ ɢɪᴠᴇ ʏᴏᴜ ᴀ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n"
        "3️⃣ ꜱʜᴀʀᴇ ᴛʜᴇ ʟɪɴᴋ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ!\n\n"
        "⚡ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴍᴏᴏɴ</i>"
    )

    await message.reply_text(
        text=help_text,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=Buttons.BACK_CLOSE_BUTTONS, # Uses your side-by-side Back/Close buttons
        disable_web_page_preview=True
    )
