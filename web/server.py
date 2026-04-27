from aiohttp import web
from info import Var   # Make sure info.py exists in the root folder

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Health check route for Koyeb"""
    return web.Response(text="Bot is running! ✅")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    """Download route"""
    file_id = request.match_info.get('file_id')
    
    # TODO: Add your actual file serving logic here later
    # For now, returning a placeholder
    return web.Response(
        text=f"Download link for file_id: {file_id}\n\nThis feature is under development.",
        content_type="text/plain"
    )


async def web_server():
    """Starts the aiohttp web server"""
    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    # Important: Use 0.0.0.0 so Koyeb can access it
    site = web.TCPSite(runner, "0.0.0.0", Var.PORT)
    await site.start()

    print(f"✅ Web server is running on port {Var.PORT}")
    return runner
