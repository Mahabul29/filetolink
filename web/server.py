import asyncio
import logging
from aiohttp import web
from config import PORT, BIN_CHANNEL

logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="Bot is running! ✅")


@routes.get("/dl/{file_id}", allow_head=True)
async def download_handler(request):
    file_id = request.match_info.get("file_id")
    file_name = request.rel_url.query.get("name", "download")

    # We will pass the main bot client from main.py instead of creating new one
    bot_client = request.app.get("bot_client")
    if not bot_client:
        return web.Response(text="Bot client not available", status=500)

    try:
        file_msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))

        if not file_msg or not (file_msg.document or file_msg.video or file_msg.audio):
            return web.Response(text="File not found.", status=404)

        media = file_msg.document or file_msg.video or file_msg.audio
        dl_name = getattr(media, "file_name", file_name)
        mime_type = getattr(media, "mime_type", "application/octet-stream")
        file_size = media.file_size

        response = web.StreamResponse(
            status=200,
            headers={
                "Content-Type": mime_type,
                "Content-Disposition": f'attachment; filename="{dl_name}"',
                "Content-Length": str(file_size),
                "Accept-Ranges": "bytes",
            }
        )
        await response.prepare(request)

        async for chunk in bot_client.stream_media(file_msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Download error for file_id {file_id}: {e}", exc_info=True)
        return web.Response(text=f"Error: {str(e)}", status=500)


async def web_server(bot_client):
    """Start web server and pass the main bot client"""
    app = web.Application()
    app["bot_client"] = bot_client          # Pass main bot client
    app["bin_channel"] = BIN_CHANNEL
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    logger.info(f"✅ Web server started on port {PORT}")
    return runner
