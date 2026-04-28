import os

# Telegram API Credentials
API_ID = int(os.environ.get("API_ID", "23787292"))
API_HASH = os.environ.get("API_HASH", "679f843b6d9485bead1b81852a9634f4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Owner & Admin
OWNER_ID = int(os.environ.get("OWNER_ID", "5733685945"))

# Channels - Power Merge Logic
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL)) 

# Database
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Web Server - Cleaned for single-slash links
FQDN = os.environ.get("FQDN", "").strip().strip("/")
PORT = int(os.environ.get("PORT", "8080"))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# Auto build base URL
BASE_URL = f"https://{FQDN}" if HAS_SSL else f"http://{FQDN}"

# Bot Username (without @)
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link2_Bot")  # ← ADD THIS
