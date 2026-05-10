import os
import asyncio
from pyrogram import Client
from aiohttp import web
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, BIN_CHANNEL, PORT, FQDN

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Udybot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("🤖 Bot session started!")

        # Peer ID Warm-up
        for channel_id in [LOG_CHANNEL, BIN_CHANNEL]:
            try:
                chat = await self.get_chat(channel_id)
                async for _ in self.get_chat_history(channel_id, limit=1):
                    break
            except Exception as e:
                print(f"⚠️ Connection Warning: {e}")

        bot_ref = self

        async def health(request):
            return web.Response(text="Bot is Running")

        # STREAMING PLAYER ROUTE
        async def video_player(request):
            file_id = request.match_info["file_id"]
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
            try:
                file_id = int(request.match_info["file_id"])
                msg = await bot_ref.get_messages(BIN_CHANNEL, file_id)
                media = msg.document or msg.video or msg.audio
                headers = {{
                    "Content-Disposition": f'attachment; filename="{{media.file_name}}"',
                    "Content-Type": media.mime_type,
                }}
                response = web.StreamResponse(headers=headers)
                await response.prepare(request)
                async for chunk in bot_ref.stream_media(msg):
                    await response.write(chunk)
                await response.write_eof()
                return response
            except:
                return web.Response(status=404)

        app = web.Application()
        app.router.add_get("/", health)
        app.router.add_get("/watch/{file_id}", video_player)
        app.router.add_get("/dl/{file_id}", stream_file)
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        await super().stop()
        
