from info import Var
import base64

async def get_link(file_id):
    # Encoding the file ID to make the link look professional
    encoded = base64.urlsafe_b64encode(file_id.encode("ascii")).decode("ascii").strip("=")
    if Var.HAS_SSL:
        return f"https://{Var.FQDN}/watch/{encoded}"
    return f"http://{Var.FQDN}:{Var.PORT}/watch/{encoded}"
  
