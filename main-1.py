import asyncio
import logging
from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return web.Response(text="Bot is running!")


@routes.get("/dl/{file_id}")
async def download_page(request):
    file_id = request.match_info["file_id"]
    try:
        msg = await bot.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio
        if media:
            file_name = getattr(media, "file_name", None) or "Unknown"
            file_size = f"{round(media.file_size / (1024 * 1024), 2)} MB"
        else:
            file_name = "Unknown"
            file_size = "Unknown"
    except Exception as e:
        logger.error(f"Download page error: {e}")
        file_name = "Unknown"
        file_size = "Unknown"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Fast Download - {file_name}</title>
  <meta http-equiv="refresh" content="2;url=/download/{file_id}">
  <style>
    body {{
      font-family: Arial, sans-serif;
      text-align: center;
      background: #121212;
      color: white;
      padding-top: 80px;
    }}
    .dl-box {{
      border: 1px solid #333;
      display: inline-block;
      padding: 40px;
      border-radius: 15px;
      background: #1e1e1e;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }}
    h3 {{ color: #4CAF50; }}
    a {{
      color: #28a745;
      text-decoration: none;
      font-weight: bold;
    }}
    .btn {{
      display: inline-block;
      background: #28a745;
      color: white;
      padding: 10px 25px;
      border-radius: 8px;
      margin-top: 15px;
      font-size: 16px;
    }}
  </style>
</head>
<body>
  <div class="dl-box">
    <h3>📁 {file_name}</h3>
    <p>📦 Size: <b>{file_size}</b></p>
    <p>⏳ Download starting automatically in 2 seconds...</p>
    <a class="btn" href="/download/{file_id}">⬇️ Click Here if Not Started</a>
  </div>
</body>
</html>"""
    return web.Response(text=html, content_type="text/html")


@routes.get("/download/{file_id}")
async def start_download(request):
    file_id = request.match_info["file_id"]
    try:
        msg = await bot.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio
        if not media:
            return web.Response(text="❌ File not found.", status=404)

        file_name = getattr(media, "file_name", None) or "download"
        mime_type = getattr(media, "mime_type", None) or "application/octet-stream"
        file_size = media.file_size

        response = web.StreamResponse(
            status=200,
            headers={
                "Content-Disposition": f'attachment; filename="{file_name}"',
                "Content-Type": mime_type,
                "Content-Length": str(file_size),
                "Accept-Ranges": "bytes",
            }
        )
        await response.prepare(request)

        async for chunk in bot.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        logger.error(f"Download error: {e}")
        return web.Response(text=f"❌ Error: {str(e)}", status=500)


async def start_web():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    logger.info(f"Web server started on port {PORT}")


async def main():
    await bot.start()
    logger.info("Bot started!")
    await start_web()
    logger.info("Listening...")
    await idle()
    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
