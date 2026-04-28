import asyncio
import logging
from bot import bot
from pyrogram import idle

logging.basicConfig(level=logging.INFO)

async def main():
    await bot.start()
    # If you have a web server for Koyeb, start it here
    # from web.server import web_server
    # await web_server(bot) 
    
    await idle() # Keeps the bot running
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
    
