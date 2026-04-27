from aiohttp import web
from config import PORT  # ✅ correct import

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Koyeb Health Check"""
    return web.Response(text="Bot is running! ✅")

@routes.get("/dl/{file_id}", allow_head=True)
async def download_handler(request):
    file_id = request.match_info.get("file_id")
    return web.Response(
        text=f"Download route for file_id: {file_id}\nFeature coming soon...",
        content_type="text/plain"
    )

async def web_server():  # ✅ no argument needed — reads from config directly
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"✅ Web server started successfully on port {PORT}")
    except OSError as e:
        print(f"❌ Failed to start web server: {e}")
        await runner.cleanup()
        raise
    return runner
