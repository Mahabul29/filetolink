from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, PORT
from aiohttp import web
import asyncio

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Udybot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        
        # This part forces the bot to 'cache' the channel ID
        try:
            # We convert the config value to an integer for the API call
            storage_chat = await self.get_chat(int(LOG_CHANNEL))
            print(f"✅ SUCCESS: Connected to {storage_chat.title} ({LOG_CHANNEL})")
        except Exception as e:
            print(f"❌ Peer ID Error: {e}")
            print("💡 TIP: Make the channel PUBLIC temporarily and send the @username to the bot.")

        # Web Server for Koyeb Health Checks
        app = web.Application()
        app.router.add_get("/", lambda r: web.Response(text="Bot is Running"))
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        asyncio.create_task(site.start())
        print(f"🚀 Health Check live on port {PORT}")

    async def stop(self, *args):
        await super().stop()
        
