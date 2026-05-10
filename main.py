import asyncio
from flask import Flask
from threading import Thread
from bot import Bot
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Alive!", 200

def run_web():
    # CHANGE THIS: Use a different port for Flask (e.g., 8000)
    # This allows your main bot server to use the required 8080
    app.run(host='0.0.0.0', port=8000)

async def start_bot():
    print("🚀 Starting Web Server for Koyeb on port 8000...")
    Thread(target=run_web, daemon=True).start()
    
    print("🤖 Bot is starting...")
    bot_instance = Bot()
    await bot_instance.start()
    
    print("✅ Bot is fully online!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        
