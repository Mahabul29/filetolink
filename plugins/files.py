from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL, FQDN, BOT_USERNAME
from plugins.utils.markup import Buttons # Importing from your new folder

def get_download_link(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    # This is the direct link that triggers the download
    download_link = f"https://{clean_host}/dl/{file_id}"
    bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
    return download_link, bot_link

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # 1. Store file in Log Channel
        copied_msg = await message.copy(chat_id=LOG_CHANNEL)

        # 2. Generate Links
        download_link, bot_link = get_download_link(copied_msg.id)

        # 3. Get file metadata
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown_File")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2)

        # 4. Generate the side-by-side buttons
        markup = Buttons.file_links(download_link, bot_link)

        # 5. Send Reply (Removed Stream Link mentions)
        await message.reply_text(
            f"<b>✅ File Stored Successfully!</b>\n\n"
            f"📁 <b>Name:</b> <code>{file_name}</code>\n"
            f"📦 <b>Size:</b> <code>{size_mb} MB</code>\n\n"
            f"🔗 <b>Download Link:</b>\n<code>{download_link}</code>\n\n"
            f"🤖 <b>Bot Link:</b>\n<code>{bot_link}</code>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
        
