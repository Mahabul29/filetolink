import os
import asyncio
import logging
from aiohttp import web
from pyrogram import Client, filters   # Added filters here

# ------------------- Logging -------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ------------------- Create Client -------------------
client = Client(
    name="filetolink",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    sleep_threshold=5,
)

# ------------------- Import & Register Start Handler -------------------
from start import start_cmd
client.add_handler((start_cmd, filters.command("start")))

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

    # Web Server for Koyeb
    app = web.Application()
    async def health_check(request):
        return web.Response(text="✅ Download Server is Active!\nBot is running successfully.")
    app.router.add_get('/', health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    print(f"🌐 Web server running on port {os.getenv('PORT', 8080)}")
    
    await asyncio.Event().wait()

# ------------------- Run -------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Critical Error: {e}")
