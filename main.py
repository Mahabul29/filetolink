import asyncio
from bot import Bot 
# If you are on Koyeb, you still need a tiny web server to stay alive
# If you aren't using a web server, make sure Koyeb health checks are OFF.

async def start_bot():
    print("🚀 Bot is starting...")
    bot_instance = Bot()
    await bot_instance.start()
    
    print("✅ Bot is running!")
    # This keeps the bot alive forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
    except Exception as e:
        print(f"❌ Error: {e}")
        
