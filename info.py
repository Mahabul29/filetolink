import os
from os import environ, getenv

class Var(object):
    name = str(getenv('name', 'File_To_Link_Bot'))
    API_ID = int(getenv('API_ID', '0'))
    API_HASH = str(getenv('API_HASH', ''))
    BOT_TOKEN = str(getenv('BOT_TOKEN', ''))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', '0'))
    DATABASE_URL = str(getenv('DATABASE_URL', ''))
    
    # Web Server Config
    PORT = int(getenv('PORT', '8080'))
    FQDN = getenv('FQDN', '0.0.0.0')
    HAS_SSL = str(getenv('HAS_SSL', 'True')).lower() in ('true', '1', 'yes')
    
    if HAS_SSL:
        URL = f"https://{FQDN.rstrip('/')}/"
    else:
        URL = f"http://{FQDN.rstrip('/')}:{PORT}/"
        
