import os

# Telegram API Credentials (Set these in Koyeb Environment Variables)
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Owner
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# Channels
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL))

# Database (optional)
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# ==================== Web Server Settings ====================
FQDN = os.environ.get("FQDN", "").strip().rstrip("/")

# Fallback if not set from Koyeb environment variables
if not FQDN:
    FQDN = "bizarre-eryn-mahavayst-3c43818f.koyeb.app"

# Clean FQDN (remove protocol if added by mistake)
FQDN = FQDN.replace("https://", "").replace("http://", "").rstrip("/")

PORT = int(os.environ.get("PORT", "8080"))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# Bot Username
BOT_USERNAME = os.environ.get("BOT_USERNAME", "").strip("@")

# Logging
LOG_LEVEL = "INFO"
