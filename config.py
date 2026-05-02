import os

# Combined channels
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002485776908"))

# ADD THIS LINE TO FIX THE ERROR
# Replace 12345678 with your actual Telegram User ID
ADMINS = [int(x) for x in os.environ.get("ADMINS", "12345678").split()]

# Other configs
FQDN = os.environ.get("FQDN", "your-app-url.koyeb.app")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "File_To_Link_2Robot")
