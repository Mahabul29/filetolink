import logging
import os
import mimetypes
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)


def _media_info(media):
    file_name = getattr(media, "file_name", "Unknown File")
    mime_type = getattr(media, "mime_type", None) or "application/octet-stream"
    file_size = getattr(media, "file_size", 0) or 0
    base_name = os.path.basename(file_name)
    root, ext = os.path.splitext(base_name)
    if not ext:
        guessed_type, _ = mimetypes.guess_type(base_name)
        if guessed_type:
            mime_type = guessed_type
            ext = mimetypes.guess_extension(guessed_type) or ""
    return file_name, base_name, root, ext, mime_type, file_size


def _is_video_playable(mime_type, file_name):
    mt = (mime_type or "").lower()
    fn = (file_name or "").lower()
    return (
        "mp4" in mt or
        "webm" in mt or
        "ogg" in mt or
        fn.endswith(".mp4") or
        fn.endswith(".webm") or
        fn.endswith(".ogv") or
        fn.endswith(".ogg")
    )


async def video_play(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_name, base_name, root, ext, mime_type, file_size = _media_info(media)
        size_mb = round(file_size / (1024 * 1024), 2)
        size_bytes = file_size
        playable = _is_video_playable(mime_type, file_name)

        if "video" in mime_type:
            icon = "🎬"
            file_type = "Video"
            if playable:
                player_tag = f"""
                <video controls autoplay playsinline preload="metadata"
                    style="width:100%;max-width:850px;border-radius:10px;background:#000;border:2px solid #2481cc;">
                    <source src="/stream/{file_id}" type="{mime_type}">
                </video>
                """
                note = ""
            else:
                player_tag = ""
                note = "<p class='warn'>⚠️ This video format may not play in browser. MP4 works best.</p>"
        elif "audio" in mime_type:
            icon = "🎵"
            file_type = "Audio"
            player_tag = f"""
            <audio controls autoplay preload="metadata"
                style="width:100%;max-width:850px;">
                <source src="/stream/{file_id}" type="{mime_type}">
            </audio>
            """
            note = ""
        else:
            icon = "📁"
            file_type = "File"
            player_tag = ""
            note = "<p class='warn'>⚠️ This file type may not play in browser. You can download it below.</p>"

    except Exception as e:
        logger.error(f"video_play error: {e}")
        file_name = "Unknown"
        base_name = "Unknown"
        root = "Unknown"
        ext = ""
        mime_type = "unknown"
        file_size = 0
        size_mb = 0
        size_bytes = 0
        playable = False
        icon = "📁"
        file_type = "File"
        player_tag = ""
        note = "<p class='warn'>⚠️ Could not fetch file info.</p>"

    clean_fqdn = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    download_url = f"https://{clean_fqdn}/dl/{file_id}"
    stream_url = f"https://{clean_fqdn}/stream/{file_id}"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{file_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0b1521;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 15px 40px;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        .title {{
            color: #2481cc;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            word-break: break-word;
            width: 100%;
            max-width: 850px;
        }}
        .info-box {{
            background: #112033;
            border: 1px solid #2481cc44;
            border-radius: 12px;
            padding: 12px 16px;
            width: 100%;
            max-width: 850px;
            margin-bottom: 15px;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #1e3a55;
            font-size: 13px;
        }}
        .info-row:last-child {{ border-bottom: none; }}
        .info-label {{ color: #7fb3d3; }}
        .info-value {{ color: #fff; font-weight: 500; text-align: right; word-break: break-all; }}
        .player-wrap {{
            position: relative;
            width: 100%;
            max-width: 850px;
            margin-bottom: 15px;
        }}
        .blue-glow {{
            position: absolute;
            left: -35px;
            top: 20%;
            width: 140px;
            height: 260px;
            background: rgba(40, 128, 255, 0.38);
            filter: blur(55px);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }}
        video, audio {{
            position: relative;
            z-index: 1;
            width: 100%;
            border-radius: 10px;
            background: #000;
        }}
        video {{ border: 2px solid #2481cc; }}
        .warn {{
            color: #f39c12;
            background: #1a1200;
            border: 1px solid #f39c1266;
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 12px;
            font-size: 13px;
            width: 100%;
            max-width: 850px;
            text-align: center;
        }}
        .top-buttons {{
            display: flex;
            gap: 10px;
            width: 100%;
            max-width: 850px;
            margin-bottom: 20px;
        }}
        .btn {{
            flex: 1;
            padding: 13px 10px;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 14px;
            text-align: center;
            border: none;
            display: inline-block;
        }}
        .btn-download {{ background: #27ae60; }}
        .btn-copy {{ background: #2481cc; cursor: pointer; }}
        .copied {{ background: #1a6aaa !important; }}
        @media (max-width: 480px) {{
            .info-row {{ font-size: 12px; }}
            .title {{ font-size: 16px; }}
            .blue-glow {{
                left: -55px;
                width: 120px;
                height: 220px;
            }}
        }}
    </style>
</head>
<body>
    <div class="title">{icon} {file_name}</div>

    <div class="info-box">
        <div class="info-row"><span class="info-label">📄 File Name</span><span class="info-value">{file_name}</span></div>
        <div class="info-row"><span class="info-label">🧾 Base Name</span><span class="info-value">{base_name}</span></div>
        <div class="info-row"><span class="info-label">🏷️ Extension</span><span class="info-value">{ext or "none"}</span></div>
        <div class="info-row"><span class="info-label">🎞️ Type</span><span class="info-value">{file_type}</span></div>
        <div class="info-row"><span class="info-label">📦 MIME</span><span class="info-value">{mime_type}</span></div>
        <div class="info-row"><span class="info-label">📏 Size</span><span class="info-value">{size_mb} MB ({size_bytes} bytes)</span></div>
        <div class="info-row"><span class="info-label">🆔 File ID</span><span class="info-value">{file_id}</span></div>
        <div class="info-row"><span class="info-label">▶ Playable</span><span class="info-value">{'Yes' if playable else 'No'}</span></div>
    </div>

    {note}
    <div class="player-wrap">
        <div class="blue-glow"></div>
        {player_tag}
    </div>

    <div class="top-buttons">
        <a href="{download_url}" class="btn btn-download">⬇ Download</a>
        <button class="btn btn-copy" onclick="copyLink()">🔗 Copy Link</button>
    </div>

    <script>
        const downloadUrl = "{download_url}";
        function copyLink() {{
            navigator.clipboard.writeText(downloadUrl).then(() => {{
                const btn = document.querySelector('.btn-copy');
                btn.textContent = '✅ Copied!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = '🔗 Copy Link';
                    btn.classList.remove('copied');
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>"""
    return web.Response(text=html, content_type="text/html")


async def stream_handler(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return web.Response(text="❌ File not found", status=404)

        file_name, _, _, _, mime_type, _ = _media_info(media)
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

        file_name, _, _, _, mime_type, _ = _media_info(media)
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
