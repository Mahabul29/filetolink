import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Client(
    "FileStreamBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)
