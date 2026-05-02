from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL, FQDN, BOT_USERNAME
from plugins.utils.markup import Buttons

def get_download_link(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    download_link = f"https://{clean_host}/dl/{file_id}"
    bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
    return download_link, bot_link

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # 1. Store file in Log Channel (using the combined LOG_CHANNEL)
        copied_msg = await message.copy(chat_id=LOG_CHANNEL)

        # 2. Generate Links
        download_link, bot_link = get_download_link(copied_msg.id)

        # 3. Get file metadata
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown_File")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2)

        # 4. Generate markup (Side-by-Side)
        markup = Buttons.file_links(download_link, bot_link)

        # 5. Send Reply (Links are outside code tags to stay blue/clickable)
        await message.reply_text(
            f"<b>✅ File Stored Successfully!</b>\n\n"
            f"📁 <b>Name:</b> <code>{file_name}</code>\n"
            f"📦 <b>Size:</b> <code>{size_mb} MB</code>\n\n"
            f"🔗 <b>Download Link:</b>\n{download_link}\n\n"
            f"🤖 <b>Bot Link:</b>\n{bot_link}",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply_text(f"❌ <b>Error:</b> <code>{e}</code>")
        
