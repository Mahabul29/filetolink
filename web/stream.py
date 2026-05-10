import logging
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)


async def video_player(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    # Fetch file info to display
    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        file_name = getattr(media, "file_name", "Unknown File")
        mime_type = getattr(media, "mime_type", "unknown")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2)

        # Determine file type for icon
        if "video" in mime_type:
            icon = "🎬"
            file_type = "Video"
        elif "audio" in mime_type:
            icon = "🎵"
            file_type = "Audio"
        else:
            icon = "📁"
            file_type = "Document"

        # Browser can only play mp4/webm natively
        can_play = any(x in mime_type for x in ["mp4", "webm", "ogg", "audio"])
        playable_note = "" if can_play else "<p class='warn'>⚠️ This format may not play in browser. Please download instead.</p>"

    except Exception as e:
        file_name = "Unknown"
        mime_type = "unknown"
        size_mb = 0
        icon = "📁"
        file_type = "File"
        can_play = False
        playable_note = "<p class='warn'>⚠️ Could not fetch file info.</p>"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{file_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0b1521;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 25px 15px;
            min-height: 100vh;
        }}
        .title {{
            color: #2481cc;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }}
        .info-box {{
            background: #112033;
            border: 1px solid #2481cc33;
            border-radius: 12px;
            padding: 15px 20px;
            width: 100%;
            max-width: 850px;
            margin-bottom: 18px;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid #1e3a55;
            font-size: 14px;
        }}
        .info-row:last-child {{ border-bottom: none; }}
        .info-label {{ color: #7fb3d3; }}
        .info-value {{ color: #ffffff; font-weight: 500; word-break: break-all; text-align: right; max-width: 60%; }}
        video, audio {{
            width: 100%;
            max-width: 850px;
            border-radius: 10px;
            border: 2px solid #2481cc;
            background: #000;
            margin-bottom: 18px;
        }}
        .warn {{
            color: #f39c12;
            background: #1a1200;
            border: 1px solid #f39c12;
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 15px;
            font-size: 14px;
            width: 100%;
            max-width: 850px;
            text-align: center;
        }}
        .buttons {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
            width: 100%;
            max-width: 850px;
        }}
        .btn {{
            flex: 1;
            min-width: 140px;
            padding: 13px 20px;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 15px;
            text-align: center;
            transition: opacity 0.2s;
        }}
        .btn:hover {{ opacity: 0.85; }}
        .btn-download {{ background: #27ae60; }}
        .btn-copy {{
            background: #2481cc;
            cursor: pointer;
            border: none;
            font-size: 15px;
        }}
        .copied {{ background: #1a6aaa !important; }}
    </style>
</head>
<body>
    <div class="title">{icon} {file_name}</div>

    <div class="info-box">
        <div class="info-row">
            <span class="info-label">📄 File Name</span>
            <span class="info-value">{file_name}</span>
        </div>
        <div class="info-row">
            <span class="info-label">📦 File Size</span>
            <span class="info-value">{size_mb} MB</span>
        </div>
        <div class="info-row">
            <span class="info-label">🎞️ Type</span>
            <span class="info-value">{file_type} ({mime_type})</span>
        </div>
        <div class="info-row">
            <span class="info-label">🆔 File ID</span>
            <span class="info-value">{file_id}</span>
        </div>
    </div>

    {playable_note}

    {'<video controls autoplay playsinline><source src="https://' + FQDN + '/stream/' + file_id + '" type="video/mp4">Your browser does not support this video.</video>' if "video" in mime_type or "audio" not in mime_type else '<audio controls autoplay><source src="https://' + FQDN + '/stream/' + file_id + '">Your browser does not support audio.</audio>'}

    <div class="buttons">
        <a href="https://{FQDN}/dl/{file_id}" class="btn btn-download">⬇ Download File</a>
        <button class="btn btn-copy" onclick="copyLink()">🔗 Copy Link</button>
    </div>

    <script>
        function copyLink() {{
            navigator.clipboard.writeText("https://{FQDN}/dl/{file_id}");
            const btn = document.querySelector('.btn-copy');
            btn.textContent = '✅ Copied!';
            btn.classList.add('copied');
            setTimeout(() => {{
                btn.textContent = '🔗 Copy Link';
                btn.classList.remove('copied');
            }}, 2000);
        }}
    </script>
</body>
</html>"""
    return web.Response(text=html_content, content_type='text/html')


async def stream_handler(request):
    """Browser streaming — sends raw bytes"""
    file_id = request.match_info.get('file_id')
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo

        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_size = getattr(media, "file_size", 0)
        mime_type = getattr(media, "mime_type", "video/mp4")

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
            "Content-Type": "video/mp4",
            "Content-Disposition": "inline",
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


async def download_handler(request):
    """Forces file download with real filename"""
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

        headers = {
            "Content-Type": mime_type,
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes",
        }

        response = web.StreamResponse(status=200, headers=headers)
        await response.prepare(request)

        async for chunk in bot_client.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Download error: {e}")
        return web.Response(text=f"❌ Error: {e}", status=500)
