import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

# --- Side-by-Side Buttons (Typewriter Font) ---
def make_channel_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    download_link = f"https://{clean_host}/dl/{file_id}"
    stream_link = f"https://{clean_host}/watch/{file_id}"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍", url=download_link),
            InlineKeyboardButton("𝚂𝚝𝚛𝚎𝚊𝚖", url=stream_link)
        ]
    ])

# Supported Media Types
_MEDIA_FILTER = (
    filters.document | filters.video | filters.audio |
    filters.photo | filters.animation | filters.video_note
)

@Client.on_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_file_handler(client, message):
    try:
        # 1. Copy to Log Channel (This generates the persistent ID for the link)
        copied = await message.copy(chat_id=LOG_CHANNEL)
        
        if not copied:
            return

        # 2. Create the Markup
        markup = make_channel_buttons(copied.id)

        # 3. Small sleep to prevent Telegram "Flood Wait" errors
        await asyncio.sleep(1)

        # 4. Add the buttons to the original post in the channel
        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=markup
        )
        
        print(f"✅ Buttons added to Channel Post: {message.id}")

    except Exception as e:
        print(f"❌ Error in Channel {message.chat.id}: {e}")

# Handle edited messages to ensure buttons stay there
@Client.on_edited_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_edit_handler(client, message):
    if not message.reply_markup:
        await channel_file_handler(client, message)
        
