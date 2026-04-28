
import asyncio
import logging
from pyrogram import idle

from bot import bot
from web.server import web_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    async with bot:
        me = await bot.get_me()
        logger.info(f"✅ Bot Started Successfully as @{me.username}")

        # Start web server with main bot client
        runner = await web_server(bot_client=bot)

        logger.info("🌐 Web server started on port 8080")

        try:
            await idle()   # Keep bot running
        finally:
            if runner:
                await runner.cleanup()
            logger.info("🛑 Bot Stopped")

if __name__ == "__main__":
    asyncio.run(main())
