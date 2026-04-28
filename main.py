import asyncio
from bot import bot
from pyrogram import idle

async def main():
    await bot.start()
    print("Keep this terminal open to keep the bot alive.")
    await idle() # This stops the script from closing immediately

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
