
from pyrogram import filters
import os
import logging

logger = logging.getLogger(__name__)

# Import your script
from Script import script   # Adjust import if file name is different

@client.on_message(filters.command("start"))
async def start_cmd(client_obj, message):
    logger.info(f"User {message.from_user.id} sent /start")
    user_name = message.from_user.first_name or "User"
    await message.reply_text(
        script.START_MSG.format(user_name),
        disable_web_page_preview=True
    )

@client.on_message(filters.media | filters.document | filters.video | filters.audio | filters.photo)
async def file_handler(client_obj, message):
    logger.info(f"Received file from user {message.from_user.id} - File name: {message.document.file_name if message.document else 'Unknown'}")
    
    try:
        # Forward file to BIN_CHANNEL
        forwarded_msg = await message.forward(int(os.getenv("BIN_CHANNEL")))
        
        # Generate direct download link (adjust the route if your code uses different path)
        file_id = forwarded_msg.id
        fqdn_clean = os.getenv("FQDN", "").replace("https://", "").replace("http://", "").rstrip("/")
        download_link = f"https://{fqdn_clean}/file/{file_id}"
        
        await message.reply_text(
            f"✅ **Your Direct Download Link**\n\n"
            f"{download_link}\n\n"
            f"🔗 Click above to download directly (high speed).",
            disable_web_page_preview=True
        )
        
        logger.info(f"Generated link for file: {download_link}")
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await message.reply_text("❌ Sorry, an error occurred while generating the link.")
