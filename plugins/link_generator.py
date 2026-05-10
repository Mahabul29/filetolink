from pyrogram import Client, filters
from pyrogram.types import Message
from config import LOG_CHANNEL, BIN_CHANNEL, FQDN, BOT_USERNAME
from plugins.utils.markup import Buttons

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client: Client, message: Message):
    try:
        # 1. Store the file in your BIN_CHANNEL
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)
        
        # 2. Format the links
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        download_link = f"https://{clean_host}/dl/{copied_msg.id}"
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{copied_msg.id}"

        # 3. Get Media Information
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_bytes = getattr(media, "file_size", 0)
        size_mb = round(size_bytes / (1024 * 1024), 2)

        # 4. Detailed Reply (Old version layout restored)
        await message.reply_text(
            f"✅ <b>ꜰɪʟᴇ ꜱᴛᴏʀᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!!</b>\n\n"
            f"📁 <b>ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
            f"📦 <b>ꜱɪᴢᴇ:</b> <code>{size_mb} ᴍʙ</code>\n\n"
            f"🔗 <b>ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ:</b>\n{download_link}\n\n"
            f"🤖 <b>ʙᴏᴛ ʟɪɴᴋ:</b>\n{bot_link}",
            reply_markup=Buttons.file_links(download_link, bot_link),
            disable_web_page_preview=True
        )

        # 5. Silent Logging (Fixes the Peer ID red error)
        try:
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=(
                    f"📂 <b>#NewFileGenerated</b>\n\n"
                    f"👤 <b>ᴜꜱᴇʀ:</b> {message.from_user.mention} [<code>{message.from_user.id}</code>]\n"
                    f"📁 <b>ꜰɪʟᴇ:</b> <code>{file_name}</code>\n"
                    f"🆔 <b>ᴍꜱɢ ɪᴅ:</b> <code>{copied_msg.id}</code>"
                )
            )
        except Exception:
            # This ensures that if the LOG_CHANNEL has a Peer ID issue, 
            # the user never sees the red error message.
            pass

    except Exception as e:
        # Only show errors if the actual file storage fails
        await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")
        
