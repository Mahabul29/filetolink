from aiohttp import web
from info import Var # Pulls PORT and other settings from your config

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    # This is the 'Health Check' response Koyeb looks for
    return web.Response(text="Bot is running! Visit the channel for links.")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    file_id = request.match_info.get('file_id')
    # Basic logic for the download path
    return web.Response(
        text=f"Fetching file ID: {file_id} from Telegram...",
        headers={"Content-Disposition": "attachment"}
    )

async def web_server():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # We use 0.0.0.0 and the PORT defined in your variables
    site = web.TCPSite(runner, "0.0.0.0", Var.PORT)
    await site.start()
    return runner
    
