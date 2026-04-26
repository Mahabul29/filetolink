import os
from os import environ, getenv

class Var(object):
    # 🚀 __Identity & Security__
    name = str(getenv('name', 'File_To_Link_Bot'))
    API_ID = int(getenv('API_ID', '23787292'))
    API_HASH = str(getenv('API_HASH', '679f843b6d9485bead1b81852a9634f4'))
    BOT_TOKEN = str(getenv('BOT_TOKEN', ''))

    # 📢 __Storage & Logs__
    # These must be numbers; '0' is used as a safe default to prevent crashes
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', '-1002378418888'))
    NEW_USER_LOG = int(getenv('NEW_USER_LOG', '-1002378418888'))
    
    # 👑 __Ownership__
    # Your ID is already here as a default
    OWNER_ID = [int(x) for x in getenv("OWNER_ID", "5733685945").split()]
    OWNER_USERNAME = str(getenv('OWNER_USERNAME', 'Mahabul201'))

    # 💾 __Database (MongoDB)__
    DATABASE_URL = str(getenv('DATABASE_URL', 'mongodb+srv://mahabul201:Mahbul288550@mahabul201.83adx.mongodb.net/?retryWrites=true&w=majority&appName=Mahabul201'))

    # 🌐 __Web Server (The link Chrome uses)__
    PORT = int(getenv('PORT', '8080'))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    HAS_SSL = str(getenv('HAS_SSL', 'True')).lower() in ('true', '1', 'yes')
    
    # FQDN is your Koyeb app link (e.g., app-name.koyeb.app)
    # This is what makes the downloads work in Chrome
    FQDN = getenv('FQDN', BIND_ADRESS)

    # 🔗 __URL Formatting__
    if HAS_SSL:
        URL = f"https://{FQDN.rstrip('/')}/"
    else:
        URL = f"http://{FQDN.rstrip('/')}:{PORT}/"

    # ⏱️ __Performance Settings__
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
  
