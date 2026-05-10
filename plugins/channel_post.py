import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

# --- Side-by-Side Buttons ---
def make_channel_buttons(file_id):
    # Clean the host name
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    download_link = f"https://{clean_host}/dl/{file_id}"
    stream_link = f"https://{clean_host}/watch/{file_id}"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 ↗", url=download_link),
            InlineKeyboardButton("𝚂𝚝𝚛𝚎𝚊𝚖 ↗", url=stream_link),
        ]
    ])

# Define what types of files the bot should react to
_MEDIA_FILTER = (
    filters.document | filters.video | filters.audio |
    filters.photo    | filters.voice | filters.animation |
    filters.video_note
)

# This handles NEW posts in the channel
@Client.on_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_file_handler(client: Client, message):
    try:
        # 1. The bot copies the file to your LOG_CHANNEL to get a unique ID
        # Note: Bot MUST be admin in LOG_CHANNEL
        copied = await message.copy(chat_id=LOG_CHANNEL)

        # 2. Create the buttons with that ID
        markup = make_channel_buttons(copied.id)

        # 3. Short delay to ensure Telegram has registered the post
        await asyncio.sleep(0.5)

        # 4. Edit the original post to add the buttons
        # Note: Bot MUST be admin in the channel with 'Edit Messages' permission
        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=markup
        )

        print(f"✅ Buttons added to channel message: {message.id}")

    except Exception as e:
        print(f"❌ Error adding buttons: {e}")

# This handles EDITED posts in the channel (to prevent removing buttons)
@Client.on_edited_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_edit_handler(client: Client, message):
    if not message.reply_markup:
        await channel_file_handler(client, message)
        
