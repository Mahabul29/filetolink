"""
channel_post.py  —  Drop into /plugins/ folder. No other changes needed.

Tested pattern: uses @app.on_message via Client instance passed by Pyrogram.
Works with Pyrogram 2.x (which this bot uses).
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ── Read BASE_URL from info.py safely ───────────────────────────────────────
try:
    from info import BASE_URL
except ImportError:
    BASE_URL = None


_MEDIA_ATTRS = (
    "document", "video", "audio", "photo",
    "voice", "video_note", "animation",
)

_MEDIA_FILTER = (
    filters.document | filters.video   | filters.audio |
    filters.photo    | filters.voice   | filters.animation |
    filters.video_note
)


def _get_file_unique_id(message):
    for attr in _MEDIA_ATTRS:
        media = getattr(message, attr, None)
        if media:
            return getattr(media, "file_unique_id", None)
    return None


def _build_keyboard(fuid: str, bot_username: str) -> InlineKeyboardMarkup:
    bot_link = f"https://t.me/{bot_username}?start={fuid}"
    dl_link  = f"{BASE_URL.rstrip('/')}/dl/{fuid}" if BASE_URL else bot_link
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Fast Download", url=dl_link)],
        [InlineKeyboardButton("🤖 Get via Bot",   url=bot_link)],
    ])


# ── Main handler ─────────────────────────────────────────────────────────────
@Client.on_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_file_handler(client: Client, message):
    try:
        fuid = _get_file_unique_id(message)
        if not fuid:
            return

        me = await client.get_me()
        keyboard = _build_keyboard(fuid, me.username)

        await asyncio.sleep(1)   # wait 1s so Telegram registers the post first
        await client.edit_message_reply_markup(
            chat_id    = message.chat.id,
            message_id = message.id,
            reply_markup = keyboard
        )
        print(f"[channel_post] ✅ Buttons added to msg {message.id} in {message.chat.title}")

    except Exception as e:
        print(f"[channel_post] ❌ Failed msg {message.id}: {e}")


@Client.on_edited_message(filters.channel & _MEDIA_FILTER, group=1)
async def channel_edit_handler(client: Client, message):
    if message.reply_markup:
        return
    await channel_file_handler(client, message)
