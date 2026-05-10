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
        # Resolve Peer ID for the storage channel
        try:
            await self.get_chat(BIN_CHANNEL)
            print("✅ Connection to Bin Channel Verified")
        except Exception as e:
            print(f"❌ Bin Channel Error: {e}")

        self.runner = await web_server(self)

    async def stop(self, *args):
        await super().stop()
        
