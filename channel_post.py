"""
channel_post.py — Auto-button plugin for FILE-TO-LINK-BOT
Place this file in your /plugins/ folder.

When the bot is added as an admin to a channel, it will automatically
detect any file posted and edit the message to add:
  🚀 Fast Download  |  🤖 Get via Bot
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import MessageMediaType

from info import (
    BOT_TOKEN,
    BASE_URL,       # e.g. "https://yourserver.com"  — your web server base URL
    # LOG_CHANNEL,  # optional: uncomment to log every processed post
)
from utils import get_file_id, get_file_unique_id   # reuse existing helpers if present


# ─────────────────────────────────────────────
# Media types we want to handle
# ─────────────────────────────────────────────
SUPPORTED_MEDIA = (
    MessageMediaType.DOCUMENT,
    MessageMediaType.VIDEO,
    MessageMediaType.AUDIO,
    MessageMediaType.PHOTO,
    MessageMediaType.VOICE,
    MessageMediaType.VIDEO_NOTE,
    MessageMediaType.ANIMATION,
)


def _extract_media(message):
    """Return the media object from a message, or None."""
    for attr in (
        "document", "video", "audio", "photo",
        "voice", "video_note", "animation", "sticker",
    ):
        media = getattr(message, attr, None)
        if media:
            return media
    return None


def build_buttons(file_id: str, bot_username: str) -> InlineKeyboardMarkup:
    """
    Build the two-button keyboard shown in the screenshot.

    Fast Download  → your web server's /dl/<file_id> endpoint
    Get via Bot    → deep-link into the bot's DM
    """
    dl_url  = f"{BASE_URL.rstrip('/')}/dl/{file_id}"
    bot_url = f"https://t.me/{bot_username}?start={file_id}"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚀 Fast Download", url=dl_url),
        ],
        [
            InlineKeyboardButton("🤖 Get via Bot", url=bot_url),
        ],
    ])


# ─────────────────────────────────────────────
# Handler: new file posted in a channel
# ─────────────────────────────────────────────
@Client.on_message(
    filters.channel & (
        filters.document | filters.video | filters.audio |
        filters.photo    | filters.voice | filters.animation
    )
)
async def handle_channel_file(client: Client, message):
    """
    Fires whenever a file is posted in a channel where the bot is admin.
    Edits the post to attach Fast-Download / Get-via-Bot buttons.
    """
    try:
        media = _extract_media(message)
        if not media:
            return

        # Use file_unique_id as the stable identifier forwarded to the web server
        file_id        = media.file_id
        file_unique_id = media.file_unique_id

        me = await client.get_me()
        buttons = build_buttons(file_unique_id, me.username)

        # Small delay to avoid hitting Telegram rate-limits on busy channels
        await asyncio.sleep(0.5)

        await message.edit_reply_markup(reply_markup=buttons)

    except Exception as e:
        # Silently skip — bot may not have edit rights, or post was already deleted
        print(f"[channel_post] Skipped {message.id}: {e}")


# ─────────────────────────────────────────────
# Handler: edited post — re-attach buttons if stripped
# ─────────────────────────────────────────────
@Client.on_edited_message(
    filters.channel & (
        filters.document | filters.video | filters.audio |
        filters.photo    | filters.voice | filters.animation
    )
)
async def handle_channel_edit(client: Client, message):
    """Re-add buttons if an admin edits and accidentally removes them."""
    if message.reply_markup:
        return  # buttons already present, nothing to do
    await handle_channel_file(client, message)
