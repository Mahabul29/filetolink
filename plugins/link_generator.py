from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BIN_CHANNEL, FQDN

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client, message):
    msg = await message.reply_text("Processing...")
    
    try:
        # Forward/Copy message to the Bin Channel
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)

        # Generate links
        download_link = f"https://{FQDN}/dl/{copied_msg.id}"
        stream_link = f"https://{FQDN}/watch/{copied_msg.id}"

        # Get file metadata
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)

        # Text using the updated fonts (Small Caps for labels, Typewriter for actions)
        text = (
            "<b>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 ♥︎</b>\n\n"
            f"<b>ғɪʟᴇ ɴᴀᴍᴇ:</b> <code>{file_name}</code>\n"
            f"<b>ғɪʟᴇ sɪᴢᴇ:</b> <code>{size_mb} MB</code>\n\n"
            f"<b>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍:</b>\n<code>{download_link}</code>\n\n"
            f"<b>𝚂𝚝𝚛𝚎𝚊𝚖:</b>\n<code>{stream_link}</code>"
        )

        # Buttons using Typewriter font and arrow icon
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 ↗", url=download_link),
                InlineKeyboardButton("𝚂𝚝𝚛𝚎𝚊𝚖 ↗", url=stream_link)
            ]
        ])

        await msg.edit_text(
            text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    except Exception as e:
        await msg.edit_text(f"Error: <code>{str(e)}</code>")
