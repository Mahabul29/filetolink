import os
import threading
import requests
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
        file_name="Your File",
        file_size="",
        file_id=file_id
    )

@app_web.route('/download/<file_id>')
def start_download(file_id):
    try:
        tg_api = f"https://api.telegram.org/bot{BOT_TOKEN}"

        # Get the message from BIN_CHANNEL
        msg_resp = requests.get(
            f"{tg_api}/getMessages",
            params={
                "chat_id": BIN_CHANNEL,
                "message_id": int(file_id)
            }
        ).json()

        # Use forwardMessage to access the file
        fwd = requests.post(
            f"{tg_api}/forwardMessage",
            json={
                "chat_id": BIN_CHANNEL,
                "from_chat_id": BIN_CHANNEL,
                "message_id": int(file_id)
            }
        ).json()

        if not fwd.get("ok"):
            return f"File not found: {fwd}", 404

        msg = fwd["result"]
        doc = (msg.get("document") or msg.get("video") or
               msg.get("audio") or msg.get("video_note"))

        if not doc:
            return "No file in this message.", 404

        tg_file_id = doc["file_id"]

        # Get download path
        file_info = requests.get(
            f"{tg_api}/getFile",
            params={"file_id": tg_file_id}
        ).json()

        if not file_info.get("ok"):
            return "File too large for direct download (>20MB). Use Telegram app.", 400

        file_path = file_info["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        return redirect(download_url)

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
