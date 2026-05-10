import logging
from aiohttp import web
from config import PORT
from web.stream import video_player, stream_handler

logger = logging.getLogger(__name__)

async def home(request):
    return web.Response(text="Bot is running ✅")

async def web_server(bot_client):
    app = web.Application()
    app["bot_client"] = bot_client
    
    # Routes
    app.router.add_get("/", home)
    app.router.add_get("/watch/{file_id}", video_player)
    app.router.add_get("/dl/{file_id}", stream_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    logger.info(f"✅ Web server started on port {PORT}")
    return runner
    
