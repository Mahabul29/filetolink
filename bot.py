from pyrogram import Client
from info import Var

# This starts the bot using the clean variables
bot = Client(
    name=Var.name,
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    workers=Var.WORKERS
)
