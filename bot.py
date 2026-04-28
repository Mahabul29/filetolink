from pyrogram import Client
import os

bot = Client(
    "my_bot_session",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    plugins=dict(root="plugins")  # <--- THIS LINE IS CRITICAL
)
