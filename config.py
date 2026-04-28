import os

# Telegram API Credentials
API_ID = int(os.environ.get("API_ID", "23787292"))
API_HASH = os.environ.get("API_HASH", "679f843b6d9485bead1b81852a9634f4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Owner & Admin
OWNER_ID = int(os.environ.get("OWNER_ID", "5733685945"))

# Channels
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL))

# Database (optional for now)
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Web Server Settings
FQDN = os.environ.get("FQDN", "").strip().rstrip("/")

# Important: Force FQDN if not set from environment
if not FQDN:
    FQDN = "your-app-name.koyeb.app"   # ← CHANGE THIS to your real Koyeb URL

PORT = int(os.environ.get("PORT", "8080"))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# Bot Username (without @ symbol)
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link2_Bot")

# Logging
LOG_LEVEL = "INFO"
