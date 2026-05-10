import os
from pyrogram import Client, filters, enums
from pyrogram.types import Message
# Added BIN_CHANNEL to the imports
from config import LOG_CHANNEL, BIN_CHANNEL, FQDN, BOT_USERNAME
from plugins.utils.markup import Buttons

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client: Client, message: Message):
    try:
        # 1. Store the file in the BIN_CHANNEL instead of the LOG_CHANNEL
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)
        
        # 2. Clean the FQDN to ensure the link format is correct
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        download_link = f"https://{clean_host}/dl/{copied_msg.id}"
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{copied_msg.id}"

        # 3. Get Media Info
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)

        # 4. Reply to user with the links
        await message.reply_text(
            f"✅ ꜰɪʟᴇ ꜱᴛᴏʀᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!!\n\n"
            f"📁 ɴᴀᴍᴇ: <code>{file_name}</code>\n"
            f"📦 ꜱɪᴢᴇ: <code>{size_mb} ᴍʙ</code>\n\n"
            f"🔗 ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ:\n{download_link}\n\n"
            f"🤖 ʙᴏᴛ ʟɪɴᴋ:\n{bot_link}",
            reply_markup=Buttons.file_links(download_link, bot_link),
            disable_web_page_preview=True
        )

        # 5. Send a text-only log to the LOG_CHANNEL for your tracking
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=(
                f"📂 <b>#NewFileGenerated</b>\n\n"
                f"👤 ᴜꜱᴇʀ: {message.from_user.mention} [<code>{message.from_user.id}</code>]\n"
                f"📁 ꜰɪʟᴇ: <code>{file_name}</code>\n"
                f"🆔 ᴍꜱɢ ɪᴅ: <code>{copied_msg.id}</code>"
            )
        )

    except Exception as e:
        await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")
      
