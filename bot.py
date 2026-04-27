import os
import asyncio
import logging
from aiohttp import web
from pyrogram import Client, filters

# ------------------- Logging -------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ------------------- Import Script -------------------
from Script import script   # Make sure Script.py exists in root

# ------------------- Create Client FIRST -------------------
client = Client(
    name="filetolink",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    sleep_threshold=5,
)

# ------------------- Handlers (AFTER client is defined) -------------------
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
    logger.info(f"Received file from user {message.from_user.id}")
    try:
        # Forward to BIN_CHANNEL
        forwarded = await message.forward(int(os.getenv("BIN_CHANNEL")))
        
        # Generate direct download link
        file_id = forwarded.id
        fqdn_clean = os.getenv("FQDN", "").replace("https://", "").replace("http://", "").rstrip("/")
        download_link = f"https://{fqdn_clean}/file/{file_id}"
        
        await message.reply_text(
            f"✅ **Your Direct Download Link**\n\n"
            f"{download_link}\n\n"
            f"🔗 Click to download directly (high speed).",
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error in file handler: {e}")
        await message.reply_text("❌ Sorry, something went wrong while generating the link.")

# ------------------- Main Function -------------------
async def main():
    print("🚀 Starting FileToLink Bot...")
    
    try:
        await client.start()
        me = await client.get_me()
        print(f"✅ Bot Started Successfully as @{me.username}")
        print(f"🔗 FQDN: {os.getenv('FQDN')}")
    except Exception as e:
        print(f"❌ Failed to start Telegram client: {e}")
        raise

    # Web server for Koyeb
    app = web.Application()
    async def health_check(request):
        return web.Response(text="✅ Download Server is Active!\nBot is running successfully.")
    app.router.add_get('/', health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    print(f"🌐 Web server running on port {os.getenv('PORT', 8080)}")
    
    await asyncio.Event().wait()  # Keep running

# ------------------- Run -------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Critical Error: {e}")
