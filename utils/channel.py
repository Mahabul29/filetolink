import logging
from pyrogram import Client
from config import BIN_CHANNEL

logger = logging.getLogger(__name__)

async def resolve_bin_channel(app: Client) -> bool:
    """
    Try multiple methods to resolve and cache the BIN_CHANNEL peer.
    Returns True if successful, False otherwise.
    """
    
    # Method 1: Direct get_chat
    try:
        chat = await app.get_chat(BIN_CHANNEL)
        logger.info(f"✅ BIN_CHANNEL resolved via get_chat: {chat.title}")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Method 1 failed: {e}")

    # Method 2: Join/resolve via invite link or username
    try:
        async for dialog in app.get_dialogs():
            if dialog.chat.id == BIN_CHANNEL:
                logger.info(f"✅ BIN_CHANNEL found in dialogs: {dialog.chat.title}")
                return True
        logger.warning("⚠️ Method 2: BIN_CHANNEL not found in dialogs")
    except Exception as e:
        logger.warning(f"⚠️ Method 2 failed: {e}")

    # Method 3: Send a test message then delete it
    try:
        msg = await app.send_message(BIN_CHANNEL, "🔄 Bot starting up — cache init")
        await msg.delete()
        logger.info("✅ BIN_CHANNEL resolved via send_message")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Method 3 failed: {e}")

    logger.error("❌ All methods failed. Check BIN_CHANNEL ID and bot admin status.")
    return False
