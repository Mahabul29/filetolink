import logging
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, BOT_USERNAME

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client, message):
    try:
        # Copy to storage channel
        copied_msg = await client.copy_message(
            chat_id=int(LOG_CHANNEL),
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        file_id = copied_msg.id
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"

        await message.reply_text(
            f"<b>✅ Link Generated!</b>\n\n🔗 <code>{bot_link}</code>",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🤖 Get via Bot", url=bot_link)
            ]]),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.channel & (filters.document | filters.video | filters.audio))
async def channel_handler(client, message):
    # Don't process the storage channel itself
    if message.chat.id == int(LOG_CHANNEL):
        return
    try:
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{message.id}"
        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🤖 Get via Bot", url=bot_link)
            ]])
        )
    except:
        pass
        
