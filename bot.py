from pyrogram import Client, filters
from pyrogram.types import Message
import info

app = Client(
    "filetolink",
    api_id=info.API_ID,
    api_hash=info.API_HASH,
    bot_token=info.BOT_TOKEN
)

@app.on_message(filters.private & filters.document | filters.video | filters.audio | filters.photo)
async def file_handler(client, message: Message):
    msg = await message.forward(info.BIN_CHANNEL)
    file_id = msg.id
    link = f"https://{info.FQDN}/dl/{file_id}"
    await message.reply(f"✅ **Your Download Link:**\n`{link}`")

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 Send me any file and I'll generate a download link!")

app.run()
