import asyncio
from flask import Flask
from threading import Thread
from bot import Bot
import os

# --- KOYEB HEALTH CHECK SERVER ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Alive!", 200

def run_web():
    # Koyeb provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT START LOGIC ---
async def start_bot():
    print("🚀 Starting Web Server for Koyeb...")
    Thread(target=run_web, daemon=True).start()
    
    print("🤖 Bot is starting...")
    bot_instance = Bot()
    await bot_instance.start()
    
    print("✅ Bot is fully online!")
    # Keeps the asyncio loop running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        
