import os

API_ID = int(os.environ.get("API_ID", "23787292"))
API_HASH = os.environ.get("API_HASH", "679f843b6d9485bead1b81852a9634f4")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8558296718:AAHODXcYwN1e-cjlk1Dcivd_xEONOltNkio")

# IDs must be integers
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))
BIN_CHANNEL = int(os.environ.get("BIN_CHANNEL", "-1002485776908"))

PORT = int(os.environ.get("PORT", "8080"))
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link2_Bot")
FQDN = os.environ.get("FQDN", "bizarre-eryn-mahavayst-3c43818f.koyeb.app")
