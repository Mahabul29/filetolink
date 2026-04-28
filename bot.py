from pyrogram import Client
import os

# We pull these from your Koyeb Environment Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

class Bot(Client):
    def __init__(self):
        super().__init__(
            "my_bot_session",  # This is the 'name'. NO 'name=' label allowed here.
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("✅ Bot Started Successfully")

    async def stop(self, *args):
        await super().stop()
        print("🛑 Bot Stopped")

bot = Bot()
