import os
import threading
from flask import Flask, render_template
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT

# 1. Setup Flask for Koyeb Health Checks
app_web = Flask(__name__, template_folder='template')

@app_web.route('/')
def index():
    # This keeps the 'Starting' circle from looping on Koyeb
    return "Bot Web Server is Running Successfully!", 200

@app_web.route('/dl/<file_id>')
def download_page(file_id):
    # This renders your dl.html inside the template folder
    return render_template('dl.html', file_name="Your File", direct_link="#")

# 2. Setup the Bot
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")  # Ensure your commands are in the 'plugins' folder
)

def run_web():
    """Function to run the web server."""
    # We use '0.0.0.0' so it's accessible externally
    app_web.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    # A. Start the bot first
    bot.start()
    print("✅ Bot started successfully!")

    # B. Start the Web Server in a separate thread (Non-blocking)
    # This is the "Magic" that fixes the silent bot issue
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    print(f"✅ Web Server active on port {PORT}")

    # C. Keep the main thread alive to listen for Telegram messages
    print("🚀 Bot is now listening for messages...")
    idle()
    
