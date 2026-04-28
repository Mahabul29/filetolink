from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

def make_buttons(file_id):
    # Ensure the link is clean and formatted correctly
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    stream_link = f"https://{clean_host}/dl/{file_id}"
    return stream_link, InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴅ", url=stream_link)]
    ])

# 1. CHANNEL HANDLER: Updates the file post in the channel automatically
@Client.on_message(filters.chat(LOG_CHANNEL) & (filters.document | filters.video | filters.audio))
async def channel_handler(client: Client, message: Message):
    try:
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown_File")
        file_size = f"{media.file_size / (1024 * 1024):.2f} MB"

        # Generate link using the message ID in the channel
        stream_link, markup = make_buttons(message.id)

        await message.edit_caption(
            caption=(
                f"<b>ғɪʟᴇ sᴛᴏʀᴇ</b>\n\n"
                f"<b>ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
                f"<b>sɪᴢᴇ:</b> <code>{file_size}</code>\n\n"
                f"ᴅᴏᴡɴʟᴏᴅ: <code>{stream_link}</code>"
            ),
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        print(f"Channel Edit Error: {e}")

# 2. PRIVATE HANDLER: Forwards file to channel when sent to Bot DM
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # Copy to channel - the channel_handler above will then catch it and add the link
        await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        await message.reply_text("<b>✅ File Sent to Channel! Link is being generated there.</b>")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        
