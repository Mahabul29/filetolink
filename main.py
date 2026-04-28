import os
from flask import Flask, render_template
from pyrogram import Client, idle  # Add 'idle' here
from config import API_ID, API_HASH, BOT_TOKEN, PORT
import threading # We need this to run both at once

app_web = Flask(__name__, template_folder='template')
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app_web.route('/')
def index():
    return "Bot Web Server is Running Successfully!", 200

@app_web.route('/dl/<file_id>')
def download_page(file_id):
    return render_template('dl.html', file_name="Your File", direct_link="#")

def run_web():
    # This runs the web server
    app_web.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    # 1. Start the bot
    bot.start()
    print("Bot Started!")

    # 2. Start the Web Server in a separate thread
    # This allows the bot to keep running in the main thread
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
    print(f"Web Server started on port {PORT}")

    # 3. Keep the bot alive
    idle()
    
