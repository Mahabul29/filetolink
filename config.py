import os

# Telegram API Credentials
API_ID = int(os.environ.get("API_ID", "23787292"))
API_HASH = os.environ.get("API_HASH", "679f843b6d9485bead1b81852a9634f4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Owner
OWNER_ID = int(os.environ.get("OWNER_ID", "5733685945"))

# Channels
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL))

# Database (optional)
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# ==================== Web Server Settings ====================
FQDN = os.environ.get("FQDN", "").strip().rstrip("/")

# Fallback if not set from Koyeb environment variables
if not FQDN:
    FQDN = "bizarre-eryn-mahavayst-3c43818f.koyeb.app"   # No trailing slash

# Clean FQDN (remove protocol if added by mistake)
FQDN = FQDN.replace("https://", "").replace("http://", "").rstrip("/")

PORT = int(os.environ.get("PORT", "8080"))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# Bot Username
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link2_Bot").strip("@")

# Logging
LOG_LEVEL = "INFO"
