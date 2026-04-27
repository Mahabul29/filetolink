import logging
from pyrogram import Client
from config import BIN_CHANNEL

logger = logging.getLogger(__name__)

async def resolve_bin_channel(app: Client) -> bool:
    """
    Resolves and verifies the BIN_CHANNEL.
    Bots CANNOT use invite links or GetDialogs — only direct ID lookup works.
    The bot MUST already be a member/admin of the channel before this runs.
    """

    # Only valid method for bots: direct get_chat by numeric ID
    try:
        chat = await app.get_chat(int(BIN_CHANNEL))
        logger.info(f"✅ BIN_CHANNEL resolved: {chat.title} (ID: {chat.id})")
        return True
    except Exception as e:
        logger.error(
            f"❌ Cannot resolve BIN_CHANNEL ({BIN_CHANNEL}). Error: {e}\n"
            f"👉 Fix checklist:\n"
            f"   1. Make sure BIN_CHANNEL is a valid numeric ID (e.g. -1001234567890)\n"
            f"   2. The bot must be an ADMIN in that channel\n"
            f"   3. Forward a message from your channel to @userinfobot to get the correct ID"
        )
        return False
        
