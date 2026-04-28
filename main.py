import asyncio
import logging
from pyrogram import idle
from bot import bot                     # Your main bot from bot.py
from web.server import web_server       # Updated web server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    async with bot:                     # This properly manages the client lifecycle
        me = await bot.get_me()
        logger.info(f"✅ Bot Started as @{me.username}")

        # Start Web Server with main bot client
        runner = await web_server(bot)   # Pass bot client here

        logger.info("🌐 Web server started")

        try:
            await idle()                 # Keep bot running
        finally:
            await runner.cleanup()
            logger.info("🛑 Web server stopped")

if __name__ == "__main__":
    asyncio.run(main())
