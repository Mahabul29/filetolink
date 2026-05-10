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

        # --- THE CORRECT PEER FIX ---
        # Bots CANNOT use get_dialogs. We use get_chat instead.
        print("🔄 Waking up channel connections...")
        for channel_id in [LOG_CHANNEL, BIN_CHANNEL]:
            try:
                # This forces the bot to recognize the channel ID
                chat = await self.get_chat(channel_id)
                # Fetching one message history 'warms up' the peer connection
                async for _ in self.get_chat_history(channel_id, limit=1):
                    break
                print(f"✅ Connection Verified: {chat.title}")
            except Exception as e:
                print(f"⚠️ Peer ID Warning for {channel_id}: {e}")

        # --- WEB SERVER SETUP ---
        bot_ref = self

        async def health(request):
            return web.Response(text="Bot is Running")

        async def stream_file(request):
            try:
                file_id = int(request.match_info["file_id"])
                msg = await bot_ref.get_messages(BIN_CHANNEL, file_id)
                
                if not msg or not msg.media:
                    return web.Response(status=404, text="File not found")

                media = msg.document or msg.video or msg.audio
                file_name = getattr(media, "file_name", "file")
                mime = getattr(media, "mime_type", "application/octet-stream")

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
        await site.start() 
        
        print(f"🚀 Health Check live on port {PORT}")
        print(f"✅ Bot is fully online!")

    async def stop(self, *args):
        await super().stop()
            
