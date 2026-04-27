import logging
from pyrogram import filters
from config import BASE_URL, LOG_CHANNEL

logger = logging.getLogger(__name__)

async def file_handler(client, message):
    try:
        # Check if Log Channel is set
        if not LOG_CHANNEL or LOG_CHANNEL == 0:
            return await message.reply_text("❌ LOG_CHANNEL ID is missing in Koyeb settings.")

        # 1. Forward the file to the LOG_CHANNEL
        # This acts as your 'File Store'
        forwarded_msg = await message.forward(LOG_CHANNEL)
        
        # 2. Get the Message ID from the forward
        # This ID is what makes the download link work
        file_id = forwarded_msg.id 

        # 3. Create the direct link
        download_link = f"{BASE_URL}/dl/{file_id}"

        # Get media details for the reply
        media = message.document or message.video or message.audio or message.photo
        file_name = getattr(media, "file_name", "File")
        
        reply_text = (
            f"<b>✅ File Stored in Log Channel!</b>\n\n"
            f"📂 <b>Name:</b> <code>{file_name}</code>\n"
            f"🔗 <b>Link:</b> <code>{download_link}</code>"
        )

        # 4. Reply to the user with the link
        await message.reply_text(reply_text, parse_mode="html")

        # 5. Send a confirmation log to the same channel
        await client.send_message(
            LOG_CHANNEL,
            f"📥 <b>File Stored</b>\n"
            f"👤 <b>User:</b> {message.from_user.mention} (<code>{message.from_user.id}</code>)\n"
            f"🔗 <b>Link:</b> {download_link}"
        )

    except Exception as e:
        logger.error(f"File Store Error: {e}")
        await message.reply_text("❌ Error: I couldn't store the file. Make sure I am an ADMIN in the Log Channel.")
        
