    async def start(self):
        await super().start()
        print("🤖 Bot session started!")

        # --- THE STARTUP HANDSHAKE ---
        # This forces the bot to 'see' its inbox and find your channels automatically
        print("🔄 Waking up channel connections...")
        try:
            # We crawl the first 20 dialogs to find your channels
            async for dialog in self.get_dialogs(limit=20):
                pass 
            
            for channel_id in [LOG_CHANNEL, BIN_CHANNEL]:
                try:
                    chat = await self.get_chat(channel_id)
                    print(f"✅ Connection Verified: {chat.title} ({channel_id})")
                    
                    # Optional: Send a heartbeat to the Log Channel only
                    if channel_id == LOG_CHANNEL:
                        await self.send_message(LOG_CHANNEL, "🚀 **Bot Restarted: Peer Connection Verified.**")
                except Exception as e:
                    print(f"⚠️ Peer ID Error for {channel_id}: {e}")
        except Exception as e:
            print(f"⚠️ Dialog fetch failed: {e}")

        # --- YOUR EXISTING WEB SERVER CODE ---
        bot_ref = self

        async def health(request):
            return web.Response(text="Bot is Running")

        async def stream_file(request):
            # ... (keep your existing stream_file logic here) ...
            pass

        app = web.Application()
        app.router.add_get("/", health)
        app.router.add_get("/dl/{file_id}", stream_file)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start() 
        
        print(f"🚀 Health Check & Stream live on port {PORT}")
        print(f"✅ Bot is fully online!")
        
