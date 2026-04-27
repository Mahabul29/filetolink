import logging
import config

logger = logging.getLogger(__name__)

BIN_CHANNEL = None  # Will be set via /setbinchannel command

def load_bin_channel():
    """Try to load from saved file first, then env var."""
    global BIN_CHANNEL
    
    # Priority 1: saved file (set via /setbinchannel)
    try:
        with open("bin_channel.txt", "r") as f:
            saved = int(f.read().strip())
            BIN_CHANNEL = saved
            config.BIN_CHANNEL = saved
            logger.info(f"📂 BIN_CHANNEL loaded from file: {saved}")
            return saved
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.warning(f"Could not read bin_channel.txt: {e}")

    # Priority 2: env var (may be wrong, don't crash)
    try:
        val = int(config.BIN_CHANNEL)
        BIN_CHANNEL = val
        return val
    except Exception:
        pass

    return None


async def resolve_bin_channel(app) -> bool:
    """Startup check — just warn, never crash."""
    channel_id = load_bin_channel()

    if not channel_id:
        logger.warning(
            "⚠️ BIN_CHANNEL not set. Send /setbinchannel to the bot to configure it."
        )
        return False

    try:
        chat = await app.get_chat(int(channel_id))
        logger.info(f"✅ BIN_CHANNEL resolved: {chat.title} (ID: {chat.id})")
        return True
    except Exception as e:
        logger.warning(
            f"⚠️ BIN_CHANNEL ({channel_id}) not accessible yet.\n"
            f"   Send /setbinchannel <id> to the bot to fix this."
        )
        return False
