import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

# --- FIX: Side-by-Side Buttons ---
def make_channel_buttons(file_id):
    clean_host  = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    bot_link    = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
    stream_link = f"https://{clean_host}/dl/{file_id}"
    
    return InlineKeyboardMarkup([
        [
            # Putting both buttons in this single list [] makes them side-by-side
            InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=stream_link),
            InlineKeyboardButton("ʙᴏᴛ",   url=bot_link)
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
        # 1. Forward to Log Channel
        copied = await client.copy_message(
            chat_id      = LOG_CHANNEL,
            from_chat_id = message.chat.id,
            message_id   = message.id
        )

        # 2. Create the horizontal markup
        markup = make_channel_buttons(copied.id)

        # 3. Small delay to ensure Telegram processed the original post
        await asyncio.sleep(1)
        
        # 4. Edit the reply markup of the post in the channel
        await client.edit_message_reply_markup(
            chat_id      = message.chat.id,
            message_id   = message.id,
            reply_markup = markup
        )

        print(f"[channel_post] ✅ Side-by-side buttons added to msg {message.id}")

    except Exception as e:
        print(f"[channel_post] ❌ Error → msg {message.id}: {e}")

@Client.on_edited_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_edit_handler(client: Client, message):
    # If it already has buttons, don't keep adding them
    if message.reply_markup:
        return
    await channel_file_handler(client, message)
    
