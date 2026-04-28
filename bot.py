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
        
        # 1. Warm up the channel to stop 'Peer id invalid' errors
        try:
            await self.get_chat(int(LOG_CHANNEL))
            print(f"✅ Storage Channel Connected: {LOG_CHANNEL}")
        except Exception as e:
            print(f"❌ Storage Error: {e}")

        # 2. Koyeb Health Check Server
        app = web.Application()
        app.router.add_get("/", lambda r: web.Response(text="Bot is Running"))
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        asyncio.create_task(site.start())
        print(f"🚀 Health Check live on port {PORT}")

    async def stop(self, *args):
        await super().stop()
        
