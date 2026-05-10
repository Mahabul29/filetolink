import logging
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)

PLAYERS = {
    "vlc": {
        "name": "VLC Player",
        "package": "org.videolan.vlc",
        "color": "linear-gradient(135deg, #ff7700, #cc5500)",
        "icon": "🟠",
    },
    "mx": {
        "name": "MX Player",
        "package": "com.mxtech.videoplayer.ad",
        "color": "linear-gradient(135deg, #1a73e8, #0d47a1)",
        "icon": "🔵",
    },
    "sp": {
        "name": "SPlayer",
        "package": "com.splayer.splayer",
        "color": "linear-gradient(135deg, #2ecc71, #1a8a47)",
        "icon": "🟢",
    },
}


async def play_handler(request):
    file_id = request.match_info.get("file_id")
    player_key = request.match_info.get("player")  # vlc / mx / sp
    bot_client = request.app["bot_client"]

    player = PLAYERS.get(player_key)
    if not player:
        return web.Response(text="❌ Unknown player", status=404)

    clean_fqdn = FQDN.replace("https://", "").replace("http://", "").rstrip("/")
    stream_url = f"https://{clean_fqdn}/stream/{file_id}"
    package = player["package"]

    # Direct intent URL - no iframe trick
    intent_url = f"intent:{stream_url}#Intent;package={package};action=android.intent.action.VIEW;type=video/mp4;end"
    market_url = f"https://play.google.com/store/apps/details?id={package}"

    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        file_name = getattr(media, "file_name", "Unknown File")
        size_mb = round(getattr(media, "file_size", 0) / (1024 * 1024), 2)
    except Exception:
        file_name = "Unknown File"
        size_mb = 0

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Open in {player['name']}</title>
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
            justify-content: center;
            min-height: 100vh;
            padding: 30px 20px;
            text-align: center;
        }}
        .icon {{ font-size: 64px; margin-bottom: 16px; }}
        .player-name {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 8px;
            background: {player['color']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .file-name {{
            color: #7fb3d3;
            font-size: 14px;
            margin-bottom: 4px;
            word-break: break-word;
            max-width: 400px;
        }}
        .file-size {{
            color: #4a7a9b;
            font-size: 13px;
            margin-bottom: 30px;
        }}
        .open-btn {{
            display: inline-block;
            padding: 16px 40px;
            border-radius: 12px;
            font-size: 17px;
            font-weight: bold;
            color: white;
            text-decoration: none;
            background: {player['color']};
            margin-bottom: 16px;
            width: 100%;
            max-width: 320px;
            transition: opacity 0.2s;
        }}
        .open-btn:hover {{ opacity: 0.85; }}
        .install-btn {{
            display: inline-block;
            padding: 13px 30px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
            color: white;
            text-decoration: none;
            background: #2c3e50;
            border: 1px solid #4a7a9b;
            width: 100%;
            max-width: 320px;
            margin-bottom: 16px;
            transition: opacity 0.2s;
        }}
        .install-btn:hover {{ opacity: 0.85; }}
        .back-btn {{
            color: #4a7a9b;
            font-size: 13px;
            text-decoration: none;
            margin-top: 10px;
        }}
        .back-btn:hover {{ color: #7fb3d3; }}
        .note {{
            color: #4a7a9b;
            font-size: 12px;
            margin-top: 20px;
            max-width: 320px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="icon">{player['icon']}</div>
    <div class="player-name">{player['name']}</div>
    <div class="file-name">📄 {file_name}</div>
    <div class="file-size">📦 {size_mb} MB</div>

    <!-- Direct intent link - opens app directly -->
    <a href="{intent_url}" class="open-btn">
        ▶ Open in {player['name']}
    </a>

    <!-- Install from Play Store -->
    <a href="{market_url}" target="_blank" class="install-btn">
        📥 Install {player['name']}
    </a>

    <a href="javascript:history.back()" class="back-btn">← Back to player page</a>

    <p class="note">
        If the app doesn't open, make sure {player['name']} is installed.
        Tap "Install" to get it from Play Store.
    </p>

    <script>
        // Auto-trigger the intent on page load
        window.onload = function() {{
            window.location.href = "{intent_url}";
        }};
    </script>
</body>
</html>"""
    return web.Response(text=html, content_type='text/html')
