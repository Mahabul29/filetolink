from aiohttp import web
from info import Var

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="Download Server is Active!")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    file_id = request.match_info.get('file_id')
    # This header tells Chrome to 'download' the file instead of playing it
    return web.Response(
        text="Fetching file from Telegram...",
        headers={"Content-Disposition": "attachment"} 
    )

async def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app
    
