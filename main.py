import asyncio
import logging
from pyrogram import idle
from bot import bot   # Import the bot from bot.py
from web.server import start_web   # We'll adjust this

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    # Start Pyrogram bot
    await bot.start()
    me = await bot.get_me()
    logger.info(f"✅ Bot Started as @{me.username}")

    # Start aiohttp web server
    await start_web()          # Make sure this function exists in web/server.py
    logger.info("🌐 Web server started on port 8080")

    # Keep everything running
    await idle()

    # Cleanup (rarely reached)
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
