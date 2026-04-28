import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, message: Message):
    try:
        # 1. Handle Deep Links (e.g., t.me/bot?start=file_511)
        if len(message.command) > 1:
            data = message.command[1]
            if data.startswith("file_"):
                try:
                    file_id = int(data.replace("file_", ""))
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=int(LOG_CHANNEL),
                        message_id=file_id
                    )
                except Exception as e:
                    logger.error(f"Deep link error: {e}")
                    await message.reply_text(
                        "<b>❌ File not found or has been deleted.</b>",
                        parse_mode=enums.ParseMode.HTML
                    )
                return  # ← Always return after deep link attempt

        # 2. Normal Welcome Message (NO photo — avoids crash)
        user_name = message.from_user.first_name if message.from_user else "User"
        welcome_text = (
            f"<b>👋 Hello {user_name}!</b>\n\n"
            "🤖 I am your <b>File to Link Bot</b>.\n\n"
            "📤 <b>How to use:</b>\n"
            "Send or forward any file/video to me and I will "
            "generate a high-speed download link instantly!\n\n"
            "<i>Powered by JavaGoat Streaming</i>"
        )
        await message.reply_text(
            welcome_text,
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        logger.error(f"CRITICAL ERROR in start_cmd: {e}")
        await message.reply_text("Something went wrong! Please try again later.")
