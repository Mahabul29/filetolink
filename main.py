import os
import threading
from flask import Flask, render_template
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT

# 1. Setup Flask for Koyeb Health Checks
app_web = Flask(__name__, template_folder='template')

@app_web.route('/')
def index():
    return "Bot Web Server is Running Successfully!", 200

@app_web.route('/dl/<file_id>')
def download_page(file_id):
    # CHANGED: We now pass file_id to the template so the button knows which file to request
    return render_template(
        'dl.html', 
        file_name="JavaGoat File", 
        file_size="Fast Download", 
        file_id=file_id
    )

# 2. Setup the Bot
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

def run_web():
    """Function to run the web server."""
    try:
        # Ensure PORT is an integer for Flask
        app_web.run(host="0.0.0.0", port=int(PORT))
    except Exception as e:
        print(f"Error starting web server: {e}")

if __name__ == "__main__":
    # A. Start the bot first
    bot.start()
    print("✅ Bot started successfully!")

    # B. Start the Web Server in a separate thread
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    print(f"✅ Web Server active on port {PORT}")

    # C. Keep the main thread alive
    print("🚀 Bot is now listening for messages...")
    idle()
    
