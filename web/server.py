from aiohttp import web
from config import PORT

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="Download Server is Active!")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    file_id = request.match_info.get('file_id')
    return web.Response(
        text="Fetching file from Telegram...",
        headers={"Content-Disposition": "attachment"}
    )

async def web_server(port=PORT):
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    return runner
