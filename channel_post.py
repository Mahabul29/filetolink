"""
channel_post.py  —  Drop into /plugins/ folder. No other changes needed.

When the bot is admin in a channel (with Edit Messages permission),
every file post will automatically get two inline buttons:
  🚀 Fast Download   →  your web server /dl/<file_unique_id>
  🤖 Get via Bot     →  bot DM deep-link
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ── Read config from info.py (same file the rest of the bot uses) ────────────
try:
    from info import BASE_URL
except ImportError:
    BASE_URL = None   # will fall back to bot-DM-only button if not set

# ── Supported media attributes ───────────────────────────────────────────────
_MEDIA_ATTRS = (
    "document", "video", "audio", "photo",
    "voice", "video_note", "animation", "sticker",
)

_MEDIA_FILTER = (
    filters.document | filters.video   | filters.audio     |
    filters.photo    | filters.voice   | filters.animation |
    filters.sticker  | filters.video_note
)


def _get_media(message):
    """Return (file_id, file_unique_id) or (None, None)."""
    for attr in _MEDIA_ATTRS:
        media = getattr(message, attr, None)
        if media:
            fid  = getattr(media, "file_id", None)
            fuid = getattr(media, "file_unique_id", None)
            return fid, fuid
    return None, None


def _build_keyboard(file_unique_id: str, bot_username: str) -> InlineKeyboardMarkup:
    """
    Build the two-button layout shown in the screenshot.
    If BASE_URL is not set in info.py, Fast Download links to the bot DM as well.
    """
    bot_link = f"https://t.me/{bot_username}?start={file_unique_id}"

    if BASE_URL:
        dl_link = f"{BASE_URL.rstrip('/')}/dl/{file_unique_id}"
    else:
        dl_link = bot_link   # fallback

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Fast Download", url=dl_link)],
        [InlineKeyboardButton("🤖 Get via Bot",   url=bot_link)],
    ])


# ── Handler: new channel post with a file ────────────────────────────────────
@Client.on_message(filters.channel & _MEDIA_FILTER)
async def on_channel_file(client: Client, message):
    try:
        file_id, file_unique_id = _get_media(message)
        if not file_unique_id:
            return

        me = await client.get_me()
        keyboard = _build_keyboard(file_unique_id, me.username)

        await asyncio.sleep(0.3)          # tiny delay to avoid flood-wait
        await message.edit_reply_markup(reply_markup=keyboard)

    except Exception as e:
        # Bot may lack edit rights — silently skip
        print(f"[channel_post] msg={message.id} skipped: {e}")


# ── Handler: re-attach buttons if an admin edits and wipes them ──────────────
@Client.on_edited_message(filters.channel & _MEDIA_FILTER)
async def on_channel_edit(client: Client, message):
    if message.reply_markup:
        return   # buttons already there
    await on_channel_file(client, message)
