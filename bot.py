import os
import asyncio
from pyrogram import Client
from aiohttp import web
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, PORT, FQDN

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

        # Force peer cache using get_chat + send a test message
        try:
            chat = await self.get_chat(LOG_CHANNEL)
            print(f"✅ Connected to: {chat.title} ({LOG_CHANNEL})")
        except Exception as e:
            print(f"❌ Peer ID Error: {e}")
            print("Action Needed: Send the channel username to the bot once!")

        # Web server
        bot_ref = self

        async def health(request):
            return web.Response(text="Bot is Running")

        async def stream_file(request):
            try:
                file_id = int(request.match_info["file_id"])
                msg = await bot_ref.get_messages(LOG_CHANNEL, file_id)
                if not msg or not msg.media:
                    return web.Response(status=404, text="File not found")

                media = msg.document or msg.video or msg.audio
                file_name = getattr(media, "file_name", "file") or "file"
                mime = getattr(media, "mime_type", "application/octet-stream")

                # Stream the file
                headers = {
                    "Content-Disposition": f'attachment; filename="{file_name}"',
                    "Content-Type": mime,
                }
                response = web.StreamResponse(headers=headers)
                await response.prepare(request)

                async for chunk in bot_ref.stream_media(msg):
                    await response.write(chunk)

                await response.write_eof()
                return response

            except Exception as e:
                return web.Response(status=500, text=str(e))

        app = web.Application()
        app.router.add_get("/", health)
        app.router.add_get("/dl/{file_id}", stream_file)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        asyncio.create_task(site.start())
        print(f"🚀 Health Check live on port {PORT}")
        print(f"🌐 Stream server live at https://{FQDN}/dl/")

    async def stop(self, *args):
        await super().stop()
