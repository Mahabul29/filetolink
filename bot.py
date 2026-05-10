import os
import asyncio
from pyrogram import Client
from aiohttp import web
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, BIN_CHANNEL, PORT
from web.stream import health, video_player, stream_file

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
        print("🤖 Bot session started!")

        # Connection Warm-up
        for channel_id in [LOG_CHANNEL, BIN_CHANNEL]:
            try:
                await self.get_chat(channel_id)
                async for _ in self.get_chat_history(channel_id, limit=1):
                    break
            except:
                pass

        # Setup Web Server
        app = web.Application()
        app['bot'] = self # This allows stream.py to access the bot client
        
        app.router.add_get("/", health)
        app.router.add_get("/watch/{file_id}", video_player)
        app.router.add_get("/dl/{file_id}", stream_file)
        
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", PORT).start()
        print(f"🚀 Web Server running on port {PORT}")

    async def stop(self, *args):
        await super().stop()
        
