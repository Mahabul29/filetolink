import os
import asyncio
import threading
from flask import Flask, render_template, Response, stream_with_context
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
        # Get Pyrogram's own loop
        bot_loop = bot.loop

        msg = asyncio.run_coroutine_threadsafe(
            bot.get_messages(BIN_CHANNEL, int(file_id)),
            bot_loop
        ).result(timeout=30)

        if not msg or not msg.document:
            return "File not found.", 404

        doc = msg.document
        file_name = doc.file_name or "download"
        mime_type = doc.mime_type or "application/octet-stream"
        file_size = doc.file_size

        def generate():
            ait = bot.stream_media(msg).__aiter__()
            while True:
                try:
                    chunk = asyncio.run_coroutine_threadsafe(
                        ait.__anext__(),
                        bot_loop
                    ).result(timeout=60)
                    yield chunk
                except StopAsyncIteration:
                    break
                except Exception as e:
                    print(f"Chunk error: {e}")
                    break

        return Response(
            stream_with_context(generate()),
            headers={
                "Content-Disposition": f'attachment; filename="{file_name}"',
                "Content-Type": mime_type,
                "Content-Length": str(file_size),
            }
        )

    except Exception as e:
        print(f"Download error: {e}")
        return f"Error: {str(e)}", 500


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
