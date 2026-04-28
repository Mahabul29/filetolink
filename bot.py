from pyrogram import Client
import os

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="filetolink",
            api_id=int(os.environ.get("API_ID")),
            api_hash=os.environ.get("API_HASH"),
            bot_token=os.environ.get("BOT_TOKEN"),
            workers=50,
            plugins=dict(root="plugins"), # THIS IS THE PART YOU ARE LIKELY MISSING
            sleep_threshold=5
        )

    async def start(self):
        await super().start()
        print("Bot started successfully")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped")

bot = Bot()
