import asyncio
import os
from flask import Flask
from threading import Thread
from bot import Bot

# Tiny server to stop Render from killing the bot
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Alive"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def start_bot():
    # Start the "keep-alive" server
    Thread(target=run_web_server, daemon=True).start()
    
    # Properly start the Pyrogram bot
    print("Starting Bot...")
    bot_instance = Bot()
    await bot_instance.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
        
