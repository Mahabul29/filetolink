
from aiohttp import web
import info   # Changed to direct import (no Var)

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Koyeb Health Check"""
    return web.Response(text="Bot is running! ✅")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    file_id = request.match_info.get('file_id')
    return web.Response(
        text=f"Download route for file_id: {file_id}\nFeature coming soon...",
        content_type="text/plain"
    )

async def web_server():
    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    # Use variables directly from info.py
    site = web.TCPSite(runner, "0.0.0.0", info.PORT)
    await site.start()

    print(f"✅ Web server started successfully on port {info.PORT}")
    return runner
