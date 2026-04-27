import os

# Telegram API Credentials
API_ID = int(os.environ.get("API_ID", "23787292")) # Hardcoded your ID as fallback
API_HASH = os.environ.get("API_HASH", "679f843b6d9485bead1b81852a9634f4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Owner & Admin
OWNER_ID = int(os.environ.get("OWNER_ID", "5733685945"))

# Channels - THE POWER MERGE
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))
# This line ensures if BIN_CHANNEL is 0, it uses LOG_CHANNEL instead
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL)) 

# Database
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Web Server - Added .strip() for safety
FQDN = os.environ.get("FQDN", "").strip().rstrip("/").replace("https://", "").replace("http://", "")
PORT = int(os.environ.get("PORT", "8080"))
HAS_SSL = os.environ.get("HAS_SSL", "True").lower() == "true"

# Bot Settings
FSUB = os.environ.get("FSUB", "False").lower() == "true"

# Start Media
START_PIC = os.environ.get("START_PIC", "")

# String Session
STRING_SESSION = os.environ.get("STRING_SESSION", "")

# Auto build base URL
if HAS_SSL:
    BASE_URL = f"https://{FQDN}"
else:
    BASE_URL = f"http://{FQDN}"
    
