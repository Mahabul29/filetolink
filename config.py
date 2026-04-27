import os

# =============================================
#              BOT CONFIGURATION
# =============================================

# Telegram API Credentials
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Owner & Admin
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# Channels
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "0"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

# Database
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Web Server
FQDN = os.environ.get("FQDN", "").rstrip("/")
PORT = int(os.environ.get("PORT", "8080"))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# Bot Settings
FSUB = os.environ.get("FSUB", "False").lower() == "true"

# Start Media
START_PIC = os.environ.get("START_PIC", "")

# =============================================
#              GENERATED VALUES
# =============================================

# Auto build base URL
if HAS_SSL:
    BASE_URL = f"https://{FQDN}"
else:
    BASE_URL = f"http://{FQDN}"
