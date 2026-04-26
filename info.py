import os
from os import getenv

class Var(object):
    API_ID = int(getenv('API_ID', '0'))
    API_HASH = getenv('API_HASH', '')
    BOT_TOKEN = getenv('BOT_TOKEN', '')
    DATABASE_URL = getenv('DATABASE_URL', '')
    BIN_CHANNEL = int(getenv('BIN_CHANNEL', '0'))
    
    # Koyeb Config
    PORT = int(getenv('PORT', '8080'))
    FQDN = getenv('FQDN', '0.0.0.0')
    HAS_SSL = getenv('HAS_SSL', 'True').lower() in ('true', '1', 'yes')
    
