import asyncio
import os
from flask import Flask
from threading import Thread
from bot import Bot

# 1. Setup a tiny Web Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    # Render provides the PORT variable automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def start_bot():
    # 2. Start the Web Server in a separate thread
    Thread(target=run_web_server, daemon=True).start()
    
    # 3. Start the Pyrogram Bot
    print("Starting Bot...")
    bot_instance = Bot()
    await bot_instance.start()
    
    # Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
        
