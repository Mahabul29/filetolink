import os
from os import environ, getenv

class Var(object):
    # Core Bot Identity
    name = str(getenv('name', 'File_To_Link_Bot'))
    API_ID = int(getenv('API_ID', '0'))
    API_HASH = str(getenv('API_HASH', ''))
    BOT_TOKEN = str(getenv('BOT_TOKEN', ''))

    # Storage and Logs
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', '0'))
    NEW_USER_LOG = int(getenv('NEW_USER_LOG', '0'))
    
    # Ownership
    OWNER_ID = [int(x) for x in getenv("OWNER_ID", "").split() if x]
    OWNER_USERNAME = str(getenv('OWNER_USERNAME', ''))

    # Database
    DATABASE_URL = str(getenv('DATABASE_URL', ''))

    # Web Server
    PORT = int(getenv('PORT', '8080'))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    HAS_SSL = str(getenv('HAS_SSL', 'True')).lower() in ('true', '1', 'yes')
    
    # Domain Configuration
    FQDN = getenv('FQDN', BIND_ADRESS)

    # Link Generation
    if HAS_SSL:
        URL = f"https://{FQDN.rstrip('/')}/"
    else:
        URL = f"http://{FQDN.rstrip('/')}:{PORT}/"

    # Performance
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    
