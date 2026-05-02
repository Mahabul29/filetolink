import os

# Core Bot Credentials
API_ID = int(os.environ.get("API_ID", "12345")) # Replace with your API ID
API_HASH = os.environ.get("API_HASH", "your_api_hash") 
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

# Combined Channel (LOG and BIN are the same)
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))

# Admin List (Required for /users and /broadcast)
ADMINS = [int(x) for x in os.environ.get("ADMINS", "12345678").split()]

# Connection Settings
PORT = int(os.environ.get("PORT", "8080"))
FQDN = os.environ.get("FQDN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link_2Robot")
