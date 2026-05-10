import logging
from aiohttp import web
from config import PORT
from web.stream import video_player, stream_handler, download_handler
from web.play import play_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def home(request):
    return web.Response(text="✅ Bot is Running!")


async def web_server(bot_client):
    app = web.Application(client_max_size=30 * 1024 * 1024)
    app["bot_client"] = bot_client

    app.router.add_get("/", home)
    app.router.add_get("/watch/{file_id}", video_player)
    app.router.add_get("/stream/{file_id}", stream_handler)
    app.router.add_get("/dl/{file_id}", download_handler)

    # Player routes: /play/vlc/884  /play/mx/884  /play/sp/884
    app.router.add_get("/play/{player}/{file_id}", play_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    logger.info(f"✅ Web server started on port {PORT}")
    return runner
