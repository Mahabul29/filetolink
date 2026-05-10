from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BIN_CHANNEL, FQDN

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def link_generator_handler(client, message):
    msg = await message.reply_text("<code>Processing...</code>")
    
    try:
        # Clean the host URL
        base_url = FQDN.replace("https://", "").replace("http://", "").strip("/")
        
        # Copy message to get the persistent ID
        copied_msg = await message.copy(chat_id=BIN_CHANNEL)

        # Final Link Construction
        download_link = f"https://{base_url}/dl/{copied_msg.id}"
        stream_link = f"https://{base_url}/watch/{copied_msg.id}"

        # Metadata
        media = message.document or message.video or message.audio
        file_name = getattr(media, "file_name", "Unknown")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)

        # UPDATED TEXT: Removed <code> from the link to make it "Openable"
        text = (
            "<b>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 ♥︎</b>\n\n"
            f"<b>𝙵𝚒𝚕𝚎 𝙽𝚊𝚖𝚎:</b> <code>{file_name}</code>\n\n\"
            f"<b>ғɪʟᴇ sɪᴢᴇ:</b> <code>{size_mb} MB</code>\n\n"
            f"<b>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍:</b>\n{download_link}" 
        )

        # Buttons stay the same
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
        await msg.edit_text(f"<b>Error:</b> <code>{str(e)}</code>")
        
