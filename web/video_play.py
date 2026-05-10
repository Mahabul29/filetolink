import logging
from aiohttp import web
from pyrogram import Client

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  In-memory store
#  MEDIA_DB[main_file_id] = {
#      "title": "...",
#      "versions": [
#          {"label": "English Sub", "file_id": "..."},
#          {"label": "Hindi Dub",   "file_id": "..."},
#      ]
#  }
# ─────────────────────────────────────────────
MEDIA_DB: dict = {}


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def get_meta(file_id: str) -> dict:
    for main_id, meta in MEDIA_DB.items():
        for v in meta["versions"]:
            if v["file_id"] == file_id:
                return meta
    return {
        "title": "Video",
        "versions": [{"label": "Default", "file_id": file_id}],
    }


def register_media(main_file_id: str, title: str, versions: list):
    MEDIA_DB[main_file_id] = {"title": title, "versions": versions}
    logger.info(f"Registered media '{title}' with {len(versions)} version(s).")


def build_lang_buttons(versions: list, active_id: str) -> str:
    html = ""
    for v in versions:
        active = "active" if v["file_id"] == active_id else ""
        html += (
            f'<button class="lang-btn {active}" '
            f'onclick="switchLang(\'{v["file_id"]}\', this)">'
            f'{v["label"]}</button>\n'
        )
    return html


def build_player_html(title: str, file_id: str, versions: list) -> str:
    lang_buttons = build_lang_buttons(versions, file_id)
    show_controls = "block" if len(versions) > 1 else "none"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg: #080b12; --surface: #0e1420; --border: #1e2840;
    --accent: #4f8ef7; --accent2: #7c5cf7;
    --text: #e8eaf0; --muted: #5a6480; --pill-bg: #141928;
  }}
  body {{ background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; min-height: 100vh; overflow-x: hidden; }}
  .video-wrap {{ position: relative; width: 100%; background: #000; line-height: 0; }}
  video {{ width: 100%; max-height: 46vh; display: block; object-fit: contain; background: #000; }}
  .loader {{ display: none; position: absolute; inset: 0; background: rgba(0,0,0,.7); align-items: center; justify-content: center; z-index: 10; }}
  .loader.show {{ display: flex; }}
  .spinner {{ width: 38px; height: 38px; border: 3px solid var(--border); border-top-color: var(--accent); border-radius: 50%; animation: spin .7s linear infinite; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .panel {{ margin: 14px; background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 18px 16px 20px; animation: fadeUp .4s ease both; }}
  @keyframes fadeUp {{ from {{ opacity:0; transform:translateY(12px); }} to {{ opacity:1; transform:translateY(0); }} }}
  .panel-title {{ font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .panel-title span {{ background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .panel-sub {{ font-size: 11px; color: var(--muted); margin-bottom: 16px; }}
  .divider {{ border: none; border-top: 1px solid var(--border); margin: 14px 0; }}
  .lang-section {{ display: {show_controls}; }}
  .section-label {{ font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
  .section-label::before {{ content: ''; display: inline-block; width: 3px; height: 12px; background: linear-gradient(var(--accent), var(--accent2)); border-radius: 2px; }}
  .lang-row {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  .lang-btn {{ background: var(--pill-bg); color: var(--text); border: 1px solid var(--border); border-radius: 50px; padding: 7px 18px; font-family: 'DM Sans', sans-serif; font-size: 12.5px; font-weight: 500; cursor: pointer; transition: background .2s, border-color .2s, color .2s, transform .1s; }}
  .lang-btn:active {{ transform: scale(.96); }}
  .lang-btn.active, .lang-btn:hover {{ background: linear-gradient(135deg, var(--accent), var(--accent2)); border-color: transparent; color: #fff; }}
  .lang-btn.active::after {{ content: '●'; font-size: 5px; vertical-align: middle; margin-left: 6px; opacity: .8; }}
  .now-playing {{ display: inline-flex; align-items: center; gap: 5px; background: rgba(79,142,247,.12); border: 1px solid rgba(79,142,247,.25); border-radius: 50px; padding: 4px 10px; font-size: 11px; color: var(--accent); margin-top: 12px; }}
  .dot {{ width: 6px; height: 6px; background: var(--accent); border-radius: 50%; animation: pulse 1.2s ease infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity:1; transform:scale(1); }} 50% {{ opacity:.4; transform:scale(.7); }} }}
</style>
</head>
<body>
<div class="video-wrap">
  <video id="player" controls autoplay playsinline>
    <source src="/stream/{file_id}" type="video/mp4">
    Your browser does not support HTML5 video.
  </video>
  <div class="loader" id="loader"><div class="spinner"></div></div>
</div>
<div class="panel">
  <div class="panel-title">Now watching — <span>{title}</span></div>
  <div class="panel-sub">Tap a language button to switch audio or subtitles</div>
  <div class="lang-section">
    <hr class="divider">
    <div class="section-label">Language / Subtitles</div>
    <div class="lang-row" id="lang-row">{lang_buttons}</div>
    <div class="now-playing" id="now-playing">
      <span class="dot"></span>
      <span id="now-label">Loading…</span>
    </div>
  </div>
</div>
<script>
  const player = document.getElementById('player');
  const loader = document.getElementById('loader');
  const nowLbl = document.getElementById('now-label');
  const firstActive = document.querySelector('.lang-btn.active');
  if (firstActive) nowLbl.textContent = firstActive.textContent.trim().replace('●','').trim();

  function switchLang(fileId, btn) {{
    loader.classList.add('show');
    player.src = '/stream/' + fileId;
    player.load();
    player.play().catch(() => {{}});
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    nowLbl.textContent = btn.textContent.trim().replace('●','').trim();
  }}
  player.addEventListener('canplay', () => loader.classList.remove('show'));
  player.addEventListener('error',   () => loader.classList.remove('show'));
</script>
</body>
</html>"""


# ─────────────────────────────────────────────
#  Route: /watch/{file_id}
# ─────────────────────────────────────────────

async def video_play(request: web.Request) -> web.Response:
    file_id = request.match_info["file_id"]
    meta = get_meta(file_id)
    html = build_player_html(meta["title"], file_id, meta["versions"])
    return web.Response(text=html, content_type="text/html")


# ─────────────────────────────────────────────
#  Route: /stream/{file_id} — real byte-range streaming
# ─────────────────────────────────────────────

async def stream_handler(request: web.Request) -> web.Response:
    file_id = request.match_info["file_id"]
    bot: Client = request.app["bot_client"]

    # parse Range header (browsers send this for video seeking)
    range_header = request.headers.get("Range", "bytes=0-")
    range_val = range_header.replace("bytes=", "").strip()
    parts = range_val.split("-")
    start = int(parts[0]) if parts[0] else 0

    # prepare streaming response
    response = web.StreamResponse(
        status=206,
        headers={
            "Content-Type":  "video/mp4",
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start}-*/*",
            "Cache-Control": "no-cache",
            "Connection":    "keep-alive",
        },
    )
    await response.prepare(request)

    try:
        async for chunk in bot.stream_media(file_id, offset=start):
            await response.write(chunk)
    except Exception as e:
        logger.warning(f"Stream stopped for {file_id}: {e}")

    return response


# ─────────────────────────────────────────────
#  Route: /dl/{file_id} — download
# ─────────────────────────────────────────────

async def download_handler(request: web.Request) -> web.Response:
    file_id = request.match_info["file_id"]
    bot: Client = request.app["bot_client"]

    response = web.StreamResponse(
        status=200,
        headers={
            "Content-Type":        "application/octet-stream",
            "Content-Disposition": f'attachment; filename="video_{file_id[:8]}.mp4"',
        },
    )
    await response.prepare(request)

    try:
        async for chunk in bot.stream_media(file_id, offset=0):
            await response.write(chunk)
    except Exception as e:
        logger.error(f"Download error for {file_id}: {e}")

    return response
