from aiohttp import web
from info import Var
import math

routes = web.RouteTableDef()

@routes.get("/download/{file_id}")
async def stream_handler(request):
    file_id = request.match_info.get('file_id')
    # Logic to fetch file from BIN_CHANNEL and stream it
    # This usually requires an active Client session
    return web.Response(text="Streaming logic initialized. Connect your Client here.")
  
