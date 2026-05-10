import os

# --- Core Bot Credentials ---
# We use empty strings or 0 as defaults so your real IDs stay private
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "") 
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# --- Database ---
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# --- Channel Configuration ---
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", 0)) 

# --- Admin Settings ---
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
ADMINS = [OWNER_ID] 

# --- Connection Settings ---
PORT = int(os.environ.get("PORT", "8080"))
FQDN = os.environ.get("FQDN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
