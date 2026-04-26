import base64
from info import Var

async def generate_download_link(message_id):
    # Encodes the message ID to create a unique URL path
    text = str(message_id).encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(text)
    base64_string = base64_bytes.decode("ascii").strip("=")
    
    if Var.HAS_SSL:
        return f"https://{Var.FQDN}/dl/{base64_string}"
    return f"http://{Var.FQDN}:{Var.PORT}/dl/{base64_string}"
  
