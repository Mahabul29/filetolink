from pyrogram import Client, filters
from pyrogram.types import Message
from config import LOG_CHANNEL, BIN_CHANNEL, FQDN, BOT_USERNAME
from plugins.utils.markup import Buttons

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client: Client, message: Message):
    try:
        # 1. Store file in BIN_CHANNEL
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)
        
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        download_link = f"https://{clean_host}/dl/{copied_msg.id}"
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{copied_msg.id}"

        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)

        # 2. Reply to user
        await message.reply_text(
            f"✅ ꜰɪʟᴇ ꜱᴛᴏʀᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!!\n\n"
            f"📁 ɴᴀᴍᴇ: <code>{file_name}</code>\n"
            f"📦 ꜱɪᴢᴇ: <code>{size_mb} ᴍʙ</code>\n\n"
            f"🔗 ʟɪɴᴋꜱ ɢᴇɴᴇʀᴀᴛᴇᴅ!",
            reply_markup=Buttons.file_links(download_link, bot_link),
            disable_web_page_preview=True
        )

        # 3. Silent Logging (Won't show error to user if this fails)
        try:
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=f"📂 #NewFile\n👤 User: {message.from_user.id}\n🆔 Msg ID: {copied_msg.id}"
            )
        except:
            pass

    except Exception as e:
        await message.reply_text(f"❌ ᴇʀʀᴏʀ: {e}")
        
