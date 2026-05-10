import os
import asyncio
from pyrogram import Client
from aiohttp import web
# Added BIN_CHANNEL to imports
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

        # --- FORCE PEER REFRESH ---
        # We check BOTH channels to ensure the bot "sees" them on startup
        for channel_id in [LOG_CHANNEL, BIN_CHANNEL]:
            try:
                chat = await self.get_chat(channel_id)
                print(f"✅ Successfully linked to: {chat.title} ({channel_id})")
                
                # Optional: Send a startup heart-beat to Log Channel only
                if channel_id == LOG_CHANNEL:
                    await self.send_message(LOG_CHANNEL, "🚀 **Bot Restarted & Connected!**")
            except Exception as e:
                print(f"❌ Peer ID Error for {channel_id}: {e}")
                print(f"💡 Fix: Make sure Bot is Admin in {channel_id} and send a text there.")

        # --- WEB SERVER SETUP ---
        bot_ref = self

        async def health(request):
            return web.Response(text="Bot is Running and Peers are Linked!")

        async def stream_file(request):
            try:
                file_id = int(request.match_info["file_id"])
                # IMPORTANT: Files are now in BIN_CHANNEL, not LOG_CHANNEL
                msg = await bot_ref.get_messages(BIN_CHANNEL, file_id)
                
                if not msg or not msg.media:
                    return web.Response(status=404, text="File not found in Bin")

                media = msg.document or msg.video or msg.audio
                file_name = getattr(media, "file_name", "file") or "file"
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
        
        # Site starts on the PORT provided by Koyeb (usually 8080)
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start() 
        
        print(f"🚀 Health Check & Stream live on port {PORT}")
        print(f"🌐 Stream URL: https://{FQDN}/dl/")
        print("✅ Bot is fully online!")

    async def stop(self, *args):
        await super().stop()
        print("🛑 Bot Stopped.")
        
