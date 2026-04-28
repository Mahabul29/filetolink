import asyncio
from aiohttp import web
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL

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
        if msg and msg.document:
            file_name = msg.document.file_name or "Unknown"
            file_size = f"{round(msg.document.file_size / (1024 * 1024), 2)} MB"
        else:
            file_name = "Unknown"
            file_size = "Unknown"
    except Exception:
        file_name = "Unknown"
        file_size = "Unknown"

    html = f"""<!DOCTYPE html>
<html>
<head><title>Fast Download</title>
<style>
body{{font-family:Arial,sans-serif;text-align:center;background:#121212;color:white;padding-top:50px}}
.dl-box{{border:1px solid #333;display:inline-block;padding:30px;border-radius:15px;background:#1e1e1e;box-shadow:0 4px 15px rgba(0,0,0,0.5)}}
</style>
<meta http-equiv="refresh" content="2;url=/download/{file_id}">
</head>
<body>
<div class="dl-box">
<h3>{file_name}</h3>
<p>Size: {file_size}</p>
<p>⏳ Download starting automatically...</p>
<p>If it doesn't start, <a href="/download/{file_id}" style="color:#28a745;">click here</a></p>
</div>
</body>
</html>"""
    return web.Response(text=html, content_type="text/html")

@routes.get("/download/{file_id}")
async def start_download(request):
    file_id = request.match_info["file_id"]
    try:
        msg = await bot.get_messages(int(BIN_CHANNEL), int(file_id))
        if not msg or not msg.document:
            return web.Response(text="File not found.", status=404)

        doc = msg.document
        file_name = doc.file_name or "download"
        mime_type = doc.mime_type or "application/octet-stream"
        file_size = doc.file_size

        response = web.StreamResponse(
            status=200,
            headers={
                "Content-Disposition": f'attachment; filename="{file_name}"',
                "Content-Type": mime_type,
                "Content-Length": str(file_size),
            }
        )
        await response.prepare(request)

        async for chunk in bot.stream_media(msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=500)


async def start_web():
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(PORT))
    await site.start()
    print(f"Web server started on port {PORT}")


async def main():
    await bot.start()
    print("Bot started!")
    await start_web()
    print("Listening...")
    await idle()
    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
