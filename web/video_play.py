import logging
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)

def _media_info(media):
    return (
        getattr(media, "file_name", "Unknown File"),
        getattr(media, "mime_type", "application/octet-stream") or "application/octet-stream",
        getattr(media, "file_size", 0) or 0,
    )

async def video_play(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_name, mime_type, file_size = _media_info(media)
        size_mb = round(file_size / (1024 * 1024), 2)

        if "video" in mime_type:
            player_tag = f'''
            <video controls autoplay playsinline preload="metadata" style="width:100%;max-width:850px;border-radius:10px;background:#000;border:2px solid #2481cc;">
                <source src="/stream/{file_id}" type="{mime_type}">
            </video>
            '''
        elif "audio" in mime_type:
            player_tag = f'''
            <audio controls autoplay preload="metadata" style="width:100%;max-width:850px;">
                <source src="/stream/{file_id}" type="{mime_type}">
            </audio>
            '''
        else:
            player_tag = "<p style='color:#f39c12;'>This file cannot play in browser.</p>"

    except Exception as e:
        logger.error(f"video_play error: {e}")
        file_name = "Unknown"
        mime_type = "unknown"
        size_mb = 0
        player_tag = "<p style='color:#f39c12;'>Error loading file.</p>"

    clean_fqdn = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    download_url = f"https://{clean_fqdn}/dl/{file_id}"

    html = f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{file_name}</title>
        <style>
            body {{ background:#0b1521;color:#fff;font-family:Arial,sans-serif;padding:20px;text-align:center; }}
            .box {{ max-width:850px;margin:auto; }}
            .info {{ background:#112033;padding:15px;border-radius:12px;margin-bottom:15px;text-align:left; }}
            .btn {{ display:inline-block;margin:8px;padding:12px 16px;border-radius:10px;text-decoration:none;color:#fff;font-weight:bold; }}
            .download {{ background:#27ae60; }}
            .copy {{ background:#2481cc; border:none; cursor:pointer; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>{file_name}</h2>
            <div class="info">
                <div>Size: {size_mb} MB</div>
                <div>Type: {mime_type}</div>
            </div>
            {player_tag}
            <div>
                <a class="btn download" href="{download_url}">Download</a>
                <button class="btn copy" onclick="navigator.clipboard.writeText('{download_url}')">Copy Link</button>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html, content_type="text/html")

async def stream_handler(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_name, mime_type, _ = _media_info(media)
        response = web.StreamResponse(status=200, headers={
            "Content-Type": mime_type if mime_type != "unknown" else "application/octet-stream",
            "Content-Disposition": f'inline; filename="{file_name}"',
        })
        await response.prepare(request)

        async for chunk in bot_client.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Stream error: {e}")
        return web.Response(text=f"❌ Error: {e}", status=500)

async def download_handler(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_name, mime_type, _ = _media_info(media)
        response = web.StreamResponse(status=200, headers={
            "Content-Type": mime_type if mime_type != "unknown" else "application/octet-stream",
            "Content-Disposition": f'attachment; filename="{file_name}"',
        })
        await response.prepare(request)

        async for chunk in bot_client.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Download error: {e}")
        return web.Response(text=f"❌ Error: {e}", status=500)
