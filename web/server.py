from aiohttp import web
from config import PORT

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Koyeb Health Check"""
    return web.Response(text="Bot is running! ✅")

@routes.get("/dl/{file_id}", allow_head=True)
async def download_handler(request):
    """
    This handles the download request. 
    It extracts the file_id from the URL.
    """
    file_id = request.match_info.get("file_id")
    
    # In a full streaming version, this is where the bot 
    # would fetch and stream the bytes.
    return web.Response(
        text=f"Request received for File ID: {file_id}\nYour download is starting...",
        content_type="text/plain"
    )

async def web_server():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"✅ Web server started on port {PORT}")
    except OSError as e:
        print(f"❌ Web server error: {e}")
        await runner.cleanup()
        raise
    return runner
    
