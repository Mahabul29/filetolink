import asyncio
import logging
from pyrogram import idle
from bot import bot                    # Main Pyrogram bot
from web.server import web_server      # aiohttp web server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    async with bot:
        me = await bot.get_me()
        logger.info(f"✅ Bot Started Successfully as @{me.username}")

        # Start web server and pass the main bot client for streaming
        runner = await web_server(bot_client=bot)

        logger.info("🌐 Web server started on port 8080")

        try:
            await idle()                    # Keep everything running
        finally:
            if runner:
                await runner.cleanup()
            logger.info("🛑 Shutdown completed")

if __name__ == "__main__":
    asyncio.run(main())
