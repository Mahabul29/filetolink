import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, BIN_CHANNEL
from web.server import web_server

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FileToLinkBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        # FIX: Resolve Peer ID for the storage channel immediately to stop 404 errors
        try:
            await self.get_chat(BIN_CHANNEL)
            print("✅ Storage Channel Connection Verified")
        except Exception as e:
            print(f"❌ Peer Resolution Failed: {e}")

        # Start Web Server
        self.runner = await web_server(self)

    async def stop(self, *args):
        await super().stop()
        if hasattr(self, "runner"):
            await self.runner.cleanup()
            
