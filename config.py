import os

# ======================== Telegram API ========================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ======================== Owner ========================
OWNER_ID = int(os.environ.get("OWNER_ID", 0))

# ======================== Channels ========================
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL))

# ======================== Database ========================
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# ======================== Web Server ========================
FQDN = os.environ.get("FQDN", "").strip().rstrip("/")
FQDN = FQDN.replace("https://", "").replace("http://", "").rstrip("/")

PORT = int(os.environ.get("PORT", 8080))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# ======================== Bot Info ========================
BOT_USERNAME = os.environ.get("BOT_USERNAME", "").strip("@")

# ======================== Features ========================
FSUB = os.environ.get("FSUB", "False").lower() == "true"

# ======================== Logging ========================
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
