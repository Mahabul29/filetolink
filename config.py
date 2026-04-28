import os
from dotenv import load_dotenv

load_dotenv()

# Mandatory Variables
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Unified Storage (LOG_CHANNEL = BIN_CHANNEL)
# Make sure this is -1002485776908 in Koyeb
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", LOG_CHANNEL))

# Connection & Branding
FQDN = os.environ.get("FQDN", "localhost")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
