import time
from pyrogram import Client, filters

# This tracks the time from when the bot script starts
BOT_START_TIME = time.time()

@Client.on_message(filters.command("data") & filters.private)
async def get_bot_uptime(client, message):
    now = time.time()
    uptime_seconds = int(now - BOT_START_TIME)
    
    days = uptime_seconds // (24 * 3600)
    uptime_seconds %= (24 * 3600)
    hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    minutes = uptime_seconds // 60
    
    await message.reply_text(
        f"📊 **Bot Statistics**\n\n"
        f"🕒 **Uptime:** {days} Days, {hours} Hours, {minutes} Minutes"
    )
    
