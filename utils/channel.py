import logging
from pyrogram import Client
from config import BIN_CHANNEL

logger = logging.getLogger(__name__)

# ✅ Private channel invite link
BIN_CHANNEL_INVITE = "https://t.me/+xxxxxxxxxx"  # paste your real link here

async def resolve_bin_channel(app: Client) -> bool:

    # Method 1: Direct get_chat by ID
    try:
        chat = await app.get_chat(BIN_CHANNEL)
        logger.info(f"✅ BIN_CHANNEL resolved: {chat.title}")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Method 1 failed: {e}")

    # Method 2: Resolve via invite link
    try:
        chat = await app.get_chat(BIN_CHANNEL_INVITE)
        logger.info(f"✅ BIN_CHANNEL resolved via invite link: {chat.title}")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Method 2 failed: {e}")

    # Method 3: Send message to force cache
    try:
        msg = await app.send_message(BIN_CHANNEL_INVITE, "🔄 init")
        await msg.delete()
        logger.info("✅ BIN_CHANNEL resolved via send_message")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Method 3 failed: {e}")

    logger.error("❌ All methods failed.")
    return False
