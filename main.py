import asyncio
import logging
from pyrogram import Client, idle
# Ensure 'bot' is the name of your Client instance in bot.py
from bot import bot 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Start the client
        await bot.start()
        me = await bot.get_me()
        logger.info(f"✅ Bot Started as @{me.username}")
        
        # We keep it simple to test connection first
        await idle()
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
    finally:
        await bot.stop()
        logger.info("🛑 Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
    
