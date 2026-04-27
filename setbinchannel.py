import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("setbinchannel") & filters.user(OWNER_ID))
async def set_bin_channel(client: Client, message: Message):
    """
    Usage:
      Step 1: Forward any message FROM your private channel to the bot
      Step 2: Bot replies with the correct ID
      Step 3: Send /setbinchannel -100xxxxxxxxxx
    """

    # If user just sent /setbinchannel with no argument — guide them
    if len(message.command) < 2:
        await message.reply_text(
            "**How to set BIN_CHANNEL:**\n\n"
            "1️⃣ Forward any message from your private channel to me\n"
            "2️⃣ I'll reply with the correct channel ID\n"
            "3️⃣ Then send:\n"
            "`/setbinchannel -100xxxxxxxxxx`\n\n"
            "Or just forward a message here and I'll detect the ID automatically."
        )
        return

    channel_id_str = message.command[1]

    # Validate format
    try:
        channel_id = int(channel_id_str)
    except ValueError:
        await message.reply_text("❌ Invalid ID. Must be a number like `-1001234567890`.")
        return

    if not channel_id_str.startswith("-100"):
        await message.reply_text(
            "⚠️ Warning: Channel IDs usually start with `-100`.\n"
            "Make sure you copied the correct ID."
        )

    # Try to access the channel
    try:
        chat = await client.get_chat(channel_id)
    except Exception as e:
        await message.reply_text(
            f"❌ Cannot access that channel.\n"
            f"Error: `{e}`\n\n"
            f"Make sure:\n"
            f"• The bot is an **admin** in the channel\n"
            f"• The ID is correct"
        )
        return

    # Save to file so it persists across the session
    try:
        with open("bin_channel.txt", "w") as f:
            f.write(str(channel_id))
    except Exception as e:
        logger.warning(f"Could not save bin_channel.txt: {e}")

    # Patch it live in memory
    import config
    config.BIN_CHANNEL = channel_id

    # Also patch utils.channel module if loaded
    try:
        import utils.channel as uc
        uc.BIN_CHANNEL = channel_id  # type: ignore
    except Exception:
        pass

    logger.info(f"✅ BIN_CHANNEL updated to {channel_id} ({chat.title})")
    await message.reply_text(
        f"✅ **BIN_CHANNEL set successfully!**\n\n"
        f"📢 Channel: `{chat.title}`\n"
        f"🆔 ID: `{channel_id}`\n\n"
        f"⚠️ **This resets on redeploy.** To make it permanent, update `BIN_CHANNEL` in your Koyeb environment variables to:\n"
        f"`{channel_id}`"
    )


@Client.on_message(filters.forwarded & filters.user(OWNER_ID) & filters.private)
async def detect_channel_id(client: Client, message: Message):
    """Auto-detect channel ID when owner forwards a message from a channel."""
    if message.forward_from_chat:
        chat = message.forward_from_chat
        if chat.type.value in ("channel", "supergroup"):
            await message.reply_text(
                f"📢 **Detected Channel:** `{chat.title}`\n"
                f"🆔 **ID:** `{chat.id}`\n\n"
                f"To set this as your BIN_CHANNEL, send:\n"
                f"`/setbinchannel {chat.id}`"
            )
