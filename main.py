import asyncio
from flask import Flask
from threading import Thread
from bot import Bot
import os
from config import LOG_CHANNEL, BIN_CHANNEL # Import your channel IDs

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Alive!", 200

def run_web():
    app.run(host='0.0.0.0', port=8000)

async def start_bot():
    print("🚀 Starting Web Server for Koyeb on port 8000...")
    Thread(target=run_web, daemon=True).start()
    
    print("🤖 Bot is starting...")
    bot_instance = Bot()
    await bot_instance.start()

    # --- THE STARTUP HANDSHAKE ---
    # This tells the bot to find your channels immediately
    print("🔄 Refreshing Peer IDs for Channels...")
    try:
        await bot_instance.get_chat(LOG_CHANNEL)
        await bot_instance.get_chat(BIN_CHANNEL)
        print("✅ Peers refreshed! Bot is connected to channels.")
    except Exception as e:
        print(f"⚠️ Peer Refresh Warning: {e}")
        print("💡 Hint: Make sure the Bot is an Admin in both channels!")
    # ------------------------------
    
    print("✅ Bot is fully online!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        
