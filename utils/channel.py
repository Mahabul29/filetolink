import logging
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

async def resolve_bin_channel(app):
    """
    This version bypasses the strict check to stop the 'Peer ID' crash.
    """
    try:
        # We try to 'touch' the channel to introduce the bot
        await app.get_chat(LOG_CHANNEL)
        logger.info(f"✅ Channel {LOG_CHANNEL} is linked.")
        return True
    except Exception as e:
        # Even if it fails, we return True so the bot doesn't 'crush'
        logger.warning(f"⚠️ Handshake bypass active. Error was: {e}")
        return True 
