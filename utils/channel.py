import logging
import config

logger = logging.getLogger(__name__)

def load_bin_channel() -> int:
    """Load BIN_CHANNEL from env var, or fall back to bin_channel.txt if saved."""
    # Try the saved file first (set via /setbinchannel command)
    try:
        with open("bin_channel.txt", "r") as f:
            saved = int(f.read().strip())
            config.BIN_CHANNEL = saved
            logger.info(f"📂 Loaded BIN_CHANNEL from file: {saved}")
            return saved
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.warning(f"Could not read bin_channel.txt: {e}")

    return config.BIN_CHANNEL


async def resolve_bin_channel(app) -> bool:
    """Verify the bot can access BIN_CHANNEL."""
    channel_id = load_bin_channel()

    try:
        chat = await app.get_chat(int(channel_id))
        logger.info(f"✅ BIN_CHANNEL resolved: {chat.title} (ID: {chat.id})")
        return True
    except Exception as e:
        logger.error(
            f"❌ Cannot resolve BIN_CHANNEL ({channel_id}). Error: {e}\n"
            f"👉 Fix options:\n"
            f"   1. Send /setbinchannel <id> to the bot (forward a channel message first to get the ID)\n"
            f"   2. Or update BIN_CHANNEL in Koyeb environment variables\n"
            f"   3. The bot must be an ADMIN in the channel"
        )
        return False
