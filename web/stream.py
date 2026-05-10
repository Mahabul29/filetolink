import logging
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)

async def video_player(request):
    file_id = request.match_info.get("file_id")
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Video Player</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #0b1521; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 30px 15px; min-height: 100vh; }}
        h3 {{ color: #2481cc; margin-bottom: 20px; }}
        video {{ width: 100%; max-width: 850px; border-radius: 10px; border: 2px solid #2481cc; background: #000; }}
        .btn {{ display: inline-block; padding: 12px 30px; background: #2481cc; color: white; text-decoration: none; border-radius: 8px; margin-top: 20px; font-weight: bold; font-size: 16px; }}
        .btn:hover {{ background: #1a6aaa; }}
    </style>
</head>
<body>
    <h3>🎬 Streaming: {file_id}</h3>
    <video controls autoplay playsinline>
        <source src="https://{FQDN}/dl/{file_id}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <br>
    <a href="https://{FQDN}/dl/{file_id}" class="btn" download>⬇ Download File</a>
</body>
</html>"""
    return web.Response(text=html_content, content_type='text/html')


async def stream_handler(request):
    file_id = request.match_info.get('file_id')
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo

        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_name = getattr(media, "file_name", "file")
        mime_type = getattr(media, "mime_type", "application/octet-stream")
        file_size = getattr(media, "file_size", 0)

        # Handle Range requests for video seeking
        range_header = request.headers.get("Range")
        offset = 0
        end = file_size - 1
        status = 200

        if range_header:
            try:
                range_val = range_header.strip().replace("bytes=", "")
                parts = range_val.split("-")
                offset = int(parts[0]) if parts[0] else 0
                end = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
                status = 206
            except Exception:
                pass

        length = end - offset + 1

        headers = {
            "Content-Type": mime_type,
            "Content-Disposition": f'inline; filename="{file_name}"',
            "Content-Length": str(length),
            "Accept-Ranges": "bytes",
        }
        if status == 206:
            headers["Content-Range"] = f"bytes {offset}-{end}/{file_size}"

        response = web.StreamResponse(status=status, headers=headers)
        await response.prepare(request)

        async for chunk in bot_client.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Stream error: {e}")
        return web.Response(text=f"❌ Error: {e}", status=500)
