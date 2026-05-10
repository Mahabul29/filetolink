from aiohttp import web
from config import BIN_CHANNEL, FQDN

async def health(request):
    return web.Response(text="Bot is Running")

async def video_player(request):
    file_id = request.match_info["file_id"]
    # Keeping your exact style for the player
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Player</title>
        <style>
            body {{ background: #0b1521; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; }}
            video {{ width: 95%; max-width: 800px; border-radius: 10px; border: 2px solid #2481cc; }}
            .dl-btn {{ display: inline-block; padding: 12px 25px; background: #2481cc; color: white; text-decoration: none; border-radius: 5px; margin-top: 25px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <video controls autoplay><source src="https://{FQDN}/dl/{file_id}" type="video/mp4"></video>
        <br><a href="https://{FQDN}/dl/{file_id}" class="dl-btn">DOWNLOAD NOW</a>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

async def stream_file(request):
    bot = request.app['bot']
    try:
        file_id = int(request.match_info["file_id"])
        msg = await bot.get_messages(BIN_CHANNEL, file_id)
        media = msg.document or msg.video or msg.audio
        
        headers = {
            "Content-Disposition": f'attachment; filename="{media.file_name}"',
            "Content-Type": media.mime_type,
        }
        
        response = web.StreamResponse(headers=headers)
        await response.prepare(request)
        
        async for chunk in bot.stream_media(msg):
            await response.write(chunk)
            
        await response.write_eof()
        return response
    except Exception as e:
        return web.Response(status=404, text=str(e))
      
