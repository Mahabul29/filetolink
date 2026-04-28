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
        logger.info(f"✅ Bot Started as @{me.username}")

        runner = await web_server(bot_client=bot)

        logger.info("🌐 Web server started on port 8080")

        try:
            await idle()
        finally:
            if runner:
                await runner.cleanup()
            logger.info("🛑 Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
