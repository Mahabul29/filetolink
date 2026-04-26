from aiohttp import web
from info import Var
from database.users_db import db

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Download Server is Active")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    file_id = request.match_info.get('file_id')
    
    # Here you would add the logic to fetch the file from Telegram
    # and send it as a 'web.Response' with headers:
    # "Content-Disposition": "attachment; filename=your_file.mp4"
    
    return web.Response(text="Download initiated. File is being fetched from Telegram...")

async def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app
    
