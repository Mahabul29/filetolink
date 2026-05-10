import os

# --- Core Bot Credentials ---
API_ID = int(os.environ.get("API_ID", "23908124"))
API_HASH = os.environ.get("API_HASH", "308a72a60a70c766b6e551cc02ee4163") 
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8756801277:AAGyHM1RrmjddYVJg8HI5vmf7ueJvwLbL3Y")

# --- Database ---
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# --- Channel Configuration ---
# LOG_CHANNEL: Only for text logs (who joined, who generated links, errors)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003755011837"))

# BIN_CHANNEL: Only for media storage (the files users upload)
# Make sure to add this ID in Koyeb or paste the real ID here
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "-1002468135790")) 

# --- Admin Settings ---
OWNER_ID = int(os.environ.get("OWNER_ID", "8762699550"))
ADMINS = [OWNER_ID] 

# --- Connection Settings ---
PORT = int(os.environ.get("PORT", "8080"))
FQDN = os.environ.get("FQDN", "systematic-kelsy-mahavayst-c729839e.koyeb.app")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link_2Robot")
