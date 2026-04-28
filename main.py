import os
import asyncio
import threading
from flask import Flask, render_template, redirect
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL

app_web = Flask(__name__, template_folder='template')

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

@app_web.route('/')
def index():
    return "Bot Web Server is Running Successfully!", 200

@app_web.route('/dl/<file_id>')
def download_page(file_id):
    return render_template(
        'dl.html',
        file_name="JavaGoat File",
        file_size="Fast Download",
        file_id=file_id
    )

@app_web.route('/download/<file_id>')
def start_download(file_id):
    try:
        loop = bot.loop
        msg = asyncio.run_coroutine_threadsafe(
            bot.get_messages(BIN_CHANNEL, int(file_id)),
            loop
        ).result(timeout=30)

        if not msg or not msg.document:
            return "File not found.", 404

        # Get direct Telegram CDN link
        url = asyncio.run_coroutine_threadsafe(
            bot.get_file_url(msg.document.file_id),
            loop
        ).result(timeout=30)

        return redirect(url)

    except Exception as e:
        print(f"Download error: {e}")
        return f"Error: {str(e)}", 500

def run_web():
    try:
        app_web.run(host="0.0.0.0", port=int(PORT))
    except Exception as e:
        print(f"Error starting web server: {e}")

if __name__ == "__main__":
    bot.start()
    print("✅ Bot started successfully!")

    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    print(f"✅ Web Server active on port {PORT}")

    print("🚀 Bot is now listening for messages...")
    idle()
