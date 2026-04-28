import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Point both to your channel ID (e.g., -1002485776908)
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "0"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", os.environ.get("BIN_CHANNEL", "0")))

# Connection and Database
FQDN = os.environ.get("FQDN", "localhost")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
