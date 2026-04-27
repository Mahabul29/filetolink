import os

API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "0"))  # private channel to store files
FQDN = os.environ.get("FQDN", "")  # your Koyeb app URL e.g. myapp.koyeb.app
PORT = int(os.environ.get("PORT", "8080"))
