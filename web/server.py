import asyncio
from aiohttp import web
from config import PORT, BOT_TOKEN, API_ID, API_HASH, BIN_CHANNEL
from pyrogram import Client
from pyrogram.errors import FloodWait

routes = web.RouteTableDef()

stream_client = None

async def get_client():
    global stream_client
    if stream_client is None or not stream_client.is_connected:
        stream_client = Client(
            "stream_session",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True
        )
        await stream_client.start()
    return stream_client

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="Bot is running! ✅")

@routes.get("/dl/{file_id}", allow_head=True)
async def download_handler(request):
    file_id = request.match_info.get("file_id")
    file_name = request.rel_url.query.get("name", "download")

    try:
        client = await get_client()

        file_msg = await client.get_messages(BIN_CHANNEL, int(file_id))

        if not file_msg or not file_msg.document:
            return web.Response(text="File not found.", status=404)

        doc = file_msg.document
        file_size = doc.file_size
        mime_type = doc.mime_type or "application/octet-stream"
        dl_name = doc.file_name or file_name

        response = web.StreamResponse(
            status=200,
            headers={
                "Content-Type": mime_type,
                "Content-Disposition": f'attachment; filename="{dl_name}"',
                "Content-Length": str(file_size),
            }
        )
        await response.prepare(request)

        async for chunk in client.stream_media(file_msg):
            await response.write(chunk)

        await response.write_eof()
        return response

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return web.Response(text="Server busy, please retry.", status=503)
    except Exception as e:
        print(f"Stream error: {e}")
        return web.Response(text=f"Error: {str(e)}", status=500)


async def web_server():
    app = web.Application()
    app["bin_channel"] = BIN_CHANNEL
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"✅ Web server started on port {PORT}")
    except OSError as e:
        print(f"❌ Web server error: {e}")
        await runner.cleanup()
        raise
    return runner
