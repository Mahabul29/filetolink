import os
import asyncio
import threading
from flask import Flask, render_template
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL
from web.download import register_download_routes

app_web = Flask(__name__, template_folder='template')

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

register_download_routes(app_web, bot, BIN_CHANNEL)

@app_web.route('/')
def index():
    return "Bot Web Server is Running Successfully!", 200

@app_web.route('/dl/<file_id>')
def download_page(file_id):
    try:
        bot_loop = bot.loop
        msg = asyncio.run_coroutine_threadsafe(
            bot.get_messages(int(BIN_CHANNEL), int(file_id)),
            bot_loop
        ).result(timeout=30)
        if msg and msg.document:
            file_name = msg.document.file_name or "Unknown"
            file_size = f"{round(msg.document.file_size / (1024 * 1024), 2)} MB"
        else:
            file_name = "Unknown"
            file_size = "Unknown"
    except Exception as e:
        file_name = "Unknown"
        file_size = "Unknown"
    return render_template(
        'dl.html',
        file_name=file_name,
        file_size=file_size,
        file_id=file_id
    )

def run_web():
    app_web.run(host="0.0.0.0", port=int(PORT), threaded=True)

if __name__ == "__main__":
    bot.start()
    print("✅ Bot started!")
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    print(f"✅ Web server active on port {PORT}")
    print("🚀 Listening...")
    idle()
    bot.stop()
