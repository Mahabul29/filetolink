import os
from flask import Flask, render_template
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, PORT

app_web = Flask(__name__, template_folder='template')
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app_web.route('/')
def index():
    return "Bot Web Server is Running Successfully!", 200

@app_web.route('/dl/<file_id>')
def download_page(file_id):
    # This matches your template/dl.html file
    return render_template('dl.html', file_name="Your File", direct_link="#")

if __name__ == "__main__":
    # Start the bot in the background
    bot.start()
    print("Bot Started!")
    
    # Start the Web Server (Koyeb needs this on port 8080)
    app_web.run(host="0.0.0.0", port=PORT)
    
