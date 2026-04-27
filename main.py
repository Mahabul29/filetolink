import os
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from info import Var
from web.server import web_server # Ensure you have created web/server.py

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="FileStreamBot",
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            bot_token=Var.BOT_TOKEN,
            workers=Var.WORKERS,
            plugins={"root": "plugins"},
            sleep_threshold=60
        )

    async def start(self):
        # 1. Start the Pyrogram Client
        await super().start()
        me = await self.get_me()
        self.username = me.username
        
        # 2. Start the Web Server (Required for Koyeb Health Checks)
        try:
            await web_server()
            print(f"🌍 Web server running on port {Var.PORT}")
        except Exception as e:
            print(f"❌ Web Server Error: {e}")

        # 3. Verify BIN_CHANNEL (Prevents the 'Peer Invalid' lock)
        try:
            await self.get_chat(Var.BIN_CHANNEL)
            print(f"📡 BIN_CHANNEL Verified: {Var.BIN_CHANNEL}")
        except Exception as e:
            print(f"⚠️ Warning: Cannot access BIN_CHANNEL. Error: {e}")
            print("💡 Tip: Make sure the bot is an ADMIN in the channel.")

        print(f"✅ Bot is Online as @{me.username}")

    async def stop(self, *args):
        await super().stop()
        print("Bot is shutting down...")

if __name__ == "__main__":
    Bot().run()
    
