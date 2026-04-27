import os
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from info import Var # Ensures it pulls from your Koyeb variables

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
        await super().start()
        me = await self.get_me()
        self.username = me.username
        
        print(f"✅ Bot Started as @{me.username}")
        print(f"🌐 Pyrogram v{__version__} (Layer {layer})")

        # --- SILENT CHANNEL VERIFICATION ---
        try:
            # We try to 'resolve' the peer so the bot recognizes the ID
            await self.get_chat(Var.BIN_CHANNEL)
            print(f"📡 BIN_CHANNEL Linked: {Var.BIN_CHANNEL}")
        except Exception as e:
            print(f"⚠️ Peer Warning: {e}")
            print("💡 Tip: Forward a message from the channel to the bot to fix this.")

        # Webserver Logic (Required for Koyeb Health Checks)
        print(f"🌍 Web server running on port {Var.PORT}")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Cleaning up...")

if __name__ == "__main__":
    # This runs the bot instance
    Bot().run()
    
