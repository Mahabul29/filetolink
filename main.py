import asyncio
import os
from flask import Flask
from threading import Thread
from bot import Bot # Ensure this matches your file structure

# Web Server for Render Health Check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def start_bot():
    # Start the web server in the background
    Thread(target=run_web_server, daemon=True).start()
    
    # Start the Bot
    print("Starting Bot Instance...")
    bot_instance = Bot()
    await bot_instance.start()
    
    # Keep the process alive
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
        
