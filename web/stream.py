from aiohttp import web
from config import FQDN

async def video_player(request):
    file_id = request.match_info["file_id"]
    # Keeping your exact player style and font layout
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stream - {file_id}</title>
        <style>
            body {{ background: #0b1521; color: white; text-align: center; font-family: sans-serif; }}
            video {{ width: 95%; max-width: 800px; margin-top: 50px; border-radius: 10px; border: 2px solid #2481cc; }}
            .btn {{ display: inline-block; padding: 12px 25px; background: #2481cc; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <video controls autoplay><source src="https://{FQDN}/dl/{file_id}" type="video/mp4"></video>
        <br><a href="https://{FQDN}/dl/{file_id}" class="btn">DOWNLOAD</a>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')
    
