import os

# Core Bot Credentials
API_ID = int(os.environ.get("API_ID", "23908124"))
API_HASH = os.environ.get("API_HASH", "308a72a60a70c766b6e551cc02ee4163") 
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8756801277:AAGyHM1RrmjddYVJg8HI5vmf7ueJvwLbL3Y")

# Database (Add this so you can start saving users!)
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Combined Channel
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003755011837"))

# Map OWNER_ID to ADMINS
# We take the OWNER_ID and put it in a list so the bot recognizes you
OWNER_ID = int(os.environ.get("OWNER_ID", "8762699550"))
ADMINS = [OWNER_ID] 

# Connection Settings
PORT = int(os.environ.get("PORT", "8080"))
FQDN = os.environ.get("FQDN", "systematic-kelsy-mahavayst-c729839e.koyeb.app")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link_2Robot")
