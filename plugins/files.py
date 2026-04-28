from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import LOG_CHANNEL, FQDN, BOT_USERNAME

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def private_handler(client: Client, message: Message):
    try:
        # Copy file to storage channel
        copied_msg = await client.copy_message(
            chat_id=LOG_CHANNEL,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
        
        file_id = copied_msg.id
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
        stream_link = f"https://{clean_host}/dl/{file_id}"

        # Buttons
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
            [InlineKeyboardButton("🤖 Get via Bot", url=bot_link)]
        ])

        await message.reply_text(
            f"<b>✅ Your Download Link is Ready!</b>\n\n🔗 <code>{bot_link}</code>",
            reply_markup=markup,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@Client.on_message(filters.channel & (filters.document | filters.video | filters.audio))
async def channel_handler(client: Client, message: Message):
    if message.chat.id == LOG_CHANNEL:
        return
    try:
        file_id = message.id
        clean_host = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
        bot_link = f"https://t.me/{BOT_USERNAME}?start=file_{file_id}"
        stream_link = f"https://{clean_host}/dl/{file_id}"

        await client.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=message.id,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Fast Download", url=stream_link)],
                [InlineKeyboardButton("🤖 Get via Bot", url=bot_link)]
            ])
        )
    except:
        pass
        
