import logging
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)


async def video_player(request):
    file_id = request.match_info.get("file_id")
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        file_name = getattr(media, "file_name", "Unknown File")
        mime_type = getattr(media, "mime_type", "unknown")
        file_size = getattr(media, "file_size", 0)
        size_mb = round(file_size / (1024 * 1024), 2)

        if "video" in mime_type:
            icon = "🎬"
            file_type = "Video"
        elif "audio" in mime_type:
            icon = "🎵"
            file_type = "Audio"
        else:
            icon = "📁"
            file_type = "Document"

        can_play = any(x in mime_type for x in ["mp4", "webm", "ogg", "audio"])
        playable_note = "" if can_play else "<p class='warn'>⚠️ This format may not play in browser. Use VLC / MX Player below.</p>"

    except Exception as e:
        logger.error(f"File info error: {e}")
        file_name = "Unknown"
        mime_type = "unknown"
        size_mb = 0
        icon = "📁"
        file_type = "File"
        can_play = False
        playable_note = "<p class='warn'>⚠️ Could not fetch file info.</p>"

    # Clean FQDN - remove any protocol prefix or trailing slash
    clean_fqdn = FQDN.replace("https://", "").replace("http://", "").rstrip("/")

    stream_url   = f"https://{clean_fqdn}/stream/{file_id}"
    download_url = f"https://{clean_fqdn}/dl/{file_id}"

    # Correct Android intent deep links
    vlc_url = f"intent:{stream_url}#Intent;package=org.videolan.vlc;action=android.intent.action.VIEW;type=video/mp4;end"
    mx_url  = f"intent:{stream_url}#Intent;package=com.mxtech.videoplayer.ad;action=android.intent.action.VIEW;type=video/mp4;end"
    sp_url  = f"intent:{stream_url}#Intent;package=com.sp.apps.splayer;action=android.intent.action.VIEW;type=video/mp4;end"

    # Video or audio player tag
    if "video" in mime_type:
        player_tag = f'<video controls autoplay playsinline><source src="{stream_url}" type="video/mp4">Your browser does not support this video.</video>'
    elif "audio" in mime_type:
        player_tag = f'<audio controls autoplay><source src="{stream_url}">Your browser does not support audio.</audio>'
    else:
        player_tag = ""

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{file_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: #0b1521;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 15px 40px;
            min-height: 100vh;
        }}
        .title {{
            color: #2481cc;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            line-height: 1.4;
            word-break: break-word;
            max-width: 850px;
            width: 100%;
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
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #1e3a55;
            font-size: 13px;
            gap: 10px;
        }}
        .info-row:last-child {{
            border-bottom: none;
        }}
        .info-label {{
            color: #7fb3d3;
            white-space: nowrap;
        }}
        .info-value {{
            color: #fff;
            font-weight: 500;
            word-break: break-all;
            text-align: right;
        }}
        video {{
            width: 100%;
            max-width: 850px;
            border-radius: 10px;
            border: 2px solid #2481cc;
            background: #000;
            margin-bottom: 15px;
        }}
        audio {{
            width: 100%;
            max-width: 850px;
            margin-bottom: 15px;
        }}
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
            transition: opacity 0.2s;
            cursor: pointer;
            border: none;
            display: inline-block;
        }}
        .btn:hover {{
            opacity: 0.85;
        }}
        .btn-download {{
            background: #27ae60;
        }}
        .btn-copy {{
            background: #2481cc;
        }}
        .copied {{
            background: #1a6aaa !important;
        }}
        .player-section {{
            width: 100%;
            max-width: 850px;
            background: #112033;
            border: 1px solid #2481cc44;
            border-radius: 14px;
            padding: 16px;
        }}
        .player-title {{
            color: #7fb3d3;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 14px;
            text-align: center;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }}
        .player-buttons {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .player-btn {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 16px 10px;
            border-radius: 14px;
            text-decoration: none;
            font-size: 13px;
            font-weight: bold;
            color: white;
            flex: 1;
            min-width: 90px;
            max-width: 150px;
            transition: opacity 0.2s, transform 0.15s;
        }}
        .player-btn:hover {{
            opacity: 0.85;
            transform: scale(1.04);
        }}
        .player-btn .icon {{
            font-size: 30px;
        }}
        .btn-vlc {{
            background: linear-gradient(135deg, #ff7700, #cc5500);
        }}
        .btn-mx {{
            background: linear-gradient(135deg, #1a73e8, #0d47a1);
        }}
        .btn-sp {{
            background: linear-gradient(135deg, #9c27b0, #6a0080);
        }}
    </style>
</head>
<body>

    <div class="title">{icon} {file_name}</div>

    <!-- File Info Box -->
    <div class="info-box">
        <div class="info-row">
            <span class="info-label">📄 File Name</span>
            <span class="info-value">{file_name}</span>
        </div>
        <div class="info-row">
            <span class="info-label">📦 Size</span>
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

    <!-- Warning if not browser-playable -->
    {playable_note}

    <!-- Browser Player -->
    {player_tag}

    <!-- Download + Copy Buttons -->
    <div class="top-buttons">
        <a href="{download_url}" class="btn btn-download">⬇ Download</a>
        <button class="btn btn-copy" onclick="copyLink()">🔗 Copy Link</button>
    </div>

    <!-- External Players -->
    <div class="player-section">
        <div class="player-title">▶ Open With External Player</div>
        <div class="player-buttons">
            <a href="{vlc_url}" class="player-btn btn-vlc">
                <span class="icon">🟠</span>
                VLC Player
            </a>
            <a href="{mx_url}" class="player-btn btn-mx">
                <span class="icon">🔵</span>
                MX Player
            </a>
            <a href="{sp_url}" class="player-btn btn-sp">
                <span class="icon">🟣</span>
                SP Player
            </a>
        </div>
    </div>

    <script>
        function copyLink() {{
            navigator.clipboard.writeText("{download_url}").then(() => {{
                const btn = document.querySelector('.btn-copy');
                btn.textContent = '✅ Copied!';
                btn.classList.add('copied');
                setTimeout(() => {{
                    btn.textContent = '🔗 Copy Link';
                    btn.classList.remove('copied');
                }}, 2000);
            }}).catch(() => {{
                // Fallback for older browsers
                const el = document.createElement('textarea');
                el.value = "{download_url}";
                document.body.appendChild(el);
                el.select();
                document.execCommand('copy');
                document.body.removeChild(el);
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
    return web.Response(text=html_content, content_type='text/html')


async def stream_handler(request):
    """Raw stream endpoint — used by browser video tag and external players"""
    file_id = request.match_info.get('file_id')
    bot_client = request.app["bot_client"]

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo

        if not media:
            return web.Response(text="❌ File not found", status=404)

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
    """Force download with real filename and mime type"""
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
