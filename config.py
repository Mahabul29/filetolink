import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "0"))
# For the download links
FQDN = os.environ.get("FQDN", "localhost") 
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
# Database
DATABASE_URL = os.environ.get("DATABASE_URL", "")
