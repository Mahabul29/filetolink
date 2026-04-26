from pyrogram import Client
from info import Var
from web.server import web_server
from aiohttp import web
import asyncio

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=Var.name,
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            bot_token=Var.BOT_TOKEN,
            workers=Var.WORKERS
        )

    async def start(self):
        await super().start()
        print("Bot Started!")
        
        # Start Web Server for Koyeb
        app = await web_server()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', Var.PORT)
        await site.start()

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped!")

Bot().run()
