import os
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from info import Var # This imports your Koyeb variables

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=Var.name,
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
            bot_token=Var.BOT_TOKEN,
            workers=Var.WORKERS,
            plugins={"root": "plugins"}, # This loads your commands
            sleep_threshold=60
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = me.username
        
        # --- FIX FOR PEER ID INVALID ---
        try:
            # Force the bot to recognize the channel at startup
            await self.get_chat(Var.BIN_CHANNEL)
            print(f"✅ BIN_CHANNEL Verified: {Var.BIN_CHANNEL}")
        except Exception as e:
            print(f"⚠️ BIN_CHANNEL Warning: {e}")
            print("Make sure the bot is ADMIN in the channel!")
        # -------------------------------

        print(f"✅ Bot Started as @{me.username}")
        print(f"🌐 Pyrogram v{__version__} (Layer {layer})")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye!")

if __name__ == "__main__":
    Bot().run()
  
