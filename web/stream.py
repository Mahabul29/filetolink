import logging
from aiohttp import web
from config import BIN_CHANNEL, FQDN

logger = logging.getLogger(__name__)

async def video_player(request):
    file_id = request.match_info.get("file_id")
    # Custom HTML player to match your request
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Player</title>
        <style>
            body {{ background: #0b1521; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; }}
            video {{ width: 95%; max-width: 800px; border-radius: 10px; border: 2px solid #2481cc; }}
            .btn {{ display: inline-block; padding: 12px 25px; background: #2481cc; color: white; text-decoration: none; border-radius: 5px; margin-top: 25px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <video controls autoplay><source src="https://{FQDN}/dl/{file_id}" type="video/mp4"></video>
        <br><a href="https://{FQDN}/dl/{file_id}" class="btn">DOWNLOAD NOW</a>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

async def stream_handler(request):
    file_id = request.match_info.get('file_id')
    bot_client = request.app["bot_client"]
    try:
        msg = await bot_client.get_messages(int(BIN_CHANNEL), int(file_id))
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return web.Response(text="File not found", status=404)

        file_name = getattr(media, "file_name", "file")
        mime_type = getattr(media, "mime_type", "application/octet-stream")
        file_size = getattr(media, "file_size", 0)

        response = web.StreamResponse(headers={
            "Content-Type": mime_type,
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Content-Length": str(file_size),
        })
        await response.prepare(request)
        async for chunk in bot_client.stream_media(msg):
            await response.write(chunk)
        await response.write_
        
