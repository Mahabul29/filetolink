import logging
from aiohttp import web
from config import PORT, BIN_CHANNEL

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Bot is running ✅")

@routes.get("/dl/{file_id}")
async def download_handler(request):
    file_id = request.match_info['file_id']
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo

        if not media:
            return web.Response(text="File not found", status=404)

        file_name = getattr(media, "file_name", "file")
        mime_type = getattr(media, "mime_type", "application/octet-stream")
        file_size = getattr(media, "file_size", 0)

        response = web.StreamResponse(
            headers={
                "Content-Type": mime_type,
                "Content-Disposition": f'attachment; filename="{file_name}"',
                "Content-Length": str(file_size),
            }
        )
        await response.prepare(request)

        async for chunk in bot_client.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Download error: {e}")
        return web.Response(text="Error occurred", status=500)


async def web_server(bot_client):
    app = web.Application()
    app["bot_client"] = bot_client
    app["bin_channel"] = BIN_CHANNEL
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    logger.info(f"✅ Web server started on port {PORT}")
    return runner
