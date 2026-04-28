from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="filetolink",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins") # This loads your start.py, files.py, etc.
        )

    async def start(self):
        await super().start()
        print("✅ Bot is Online!")

    async def stop(self, *args):
        await super().stop()
        print("🛑 Bot Stopped!")

bot = Bot()
