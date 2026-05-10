import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN

# --- Side-by-Side Buttons ---
def make_channel_buttons(file_id):
    # Ensure FQDN doesn't have extra slashes or protocols
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
        # Copy to Log Channel to get a persistent File ID/Message ID
        copied = await message.copy(chat_id=LOG_CHANNEL)

        # Check if copy was successful and get the ID
        if not copied:
            print(f"Failed to copy message {message.id}")
            return

        markup = make_channel_buttons(copied.id)

        # Adding a small delay helps avoid race conditions with Telegram's server
        await asyncio.sleep(0.5)

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
    # Avoid infinite loops: only add markup if it doesn't already exist
    if message.reply_markup:
        return
    await channel_file_handler(client, message)
