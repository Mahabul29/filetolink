import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

# --- Side-by-Side Buttons ---
def make_channel_buttons(file_id):
    clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    download_link = f"https://{clean_host}/dl/{file_id}"
    stream_link = f"https://{clean_host}/watch/{file_id}"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download_link),
            InlineKeyboardButton("sᴛʀᴇᴀᴍ", url=stream_link),
        ]
    ])

_MEDIA_FILTER = (
    filters.document | filters.video | filters.audio |
    filters.photo    | filters.voice | filters.animation |
    filters.video_note
)

@Client.on_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_file_handler(client: Client, message):
    try:
        copied = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )

        markup = make_channel_buttons(copied.id)

        await asyncio.sleep(1)

        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=markup
        )

        print(f"[channel_post] ✅ Buttons added to msg {message.id}")

    except Exception as e:
        print(f"[channel_post] ❌ Error → msg {message.id}: {e}")

@Client.on_edited_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_edit_handler(client: Client, message):
    if message.reply_markup:
        return
    await channel_file_handler(client, message)
