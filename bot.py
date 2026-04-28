from pyrogram import Client
import os

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="filetolink",
            api_id=int(os.environ.get("API_ID")),
            api_hash=os.environ.get("API_HASH"),
            bot_token=os.environ.get("BOT_TOKEN"),
            plugins=dict(root="plugins") # THIS TELLS THE BOT WHERE THE CODE IS
        )

bot = Bot()
