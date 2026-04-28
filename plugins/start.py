import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    try:
        if len(message.command) > 1:
            data = message.command[1]
            if data.startswith("file_"):
                try:
                    file_id = int(data.split("_")[1])
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=int(LOG_CHANNEL),
                        message_id=file_id
                    )
                except Exception as e:
                    logger.error(f"Deep link error: {e}")
                    await message.reply_text(
                        "<b>❌ File not found or deleted.</b>",
                        parse_mode=enums.ParseMode.HTML
                    )
                return  # ← always return, stop here

        # Normal /start — no deep link
        user_name = message.from_user.first_name if message.from_user else "User"
        await message.reply_text(
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 Send or forward any file to me and I will "
            "generate a high-speed download link instantly!\n\n"
            "<i>Powered by JavaGoat Streaming</i>",
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Start handler error: {e}")
        await message.reply_text("Something went wrong! Please try again later.")
