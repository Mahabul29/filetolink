import base64
from info import Var

async def get_download_link(message_id):
    # Shorten/Encode the ID for the URL
    text = str(message_id).encode("ascii")
    encoded = base64.urlsafe_b64encode(text).decode("ascii").strip("=")
    
    prefix = "https://" if Var.HAS_SSL else "http://"
    return f"{prefix}{Var.FQDN}/dl/{encoded}"
    
