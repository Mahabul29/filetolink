import asyncio
from bot import Bot # Use the import style from your specific repo

async def start_bot():
    print("Starting Bot...")
    bot_instance = Bot()
    await bot_instance.start()
    
    # This keeps the bot running without a second server
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
        
