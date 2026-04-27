import os
import asyncio
import logging
from aiohttp import web
from pyrogram import Client, filters   # Make sure these imports are at the top too

# ------------------- Your existing code (Client definition) -------------------
# Make sure you have this somewhere near the top (before main):

client = Client(
    name="filetolink",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    sleep_threshold=5,
    plugins=dict(root="plugins") if os.path.exists("plugins") else None,  # if you have plugins folder
)

# ------------------- Simple /start command (add if missing) -------------------
@client.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "Send me any file (video, document, photo, etc.)\n"
        "I will give you a **direct download link**."
    )

# ------------------- Main Startup Function -------------------
async def main():
    print("🚀 Starting FileToLink Bot...")
    
    try:
        await client.start()
        me = await client.get_me()
        print(f"✅ Bot Started Successfully as @{me.username}")
        print(f"🔗 FQDN: {os.getenv('FQDN')}")
    except Exception as e:
        print(f"❌ Failed to start Telegram client: {e}")
        raise

    # Dummy web server for Koyeb (keeps the app healthy)
    app = web.Application()
    async def health_check(request):
        return web.Response(text="✅ Bot is running!")
    app.router.add_get('/', health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    print(f"🌐 Web server is running on port {os.getenv('PORT', 8080)}")
    
    # Keep the bot alive
    await asyncio.Event().wait()

# ------------------- Run the bot -------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Critical Error starting bot: {e}")
