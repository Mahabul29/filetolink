    async def start(self):
        await super().start()
        print("🤖 Bot session started!")

        # --- THE ULTIMATE PEER FIX ---
        from config import LOG_CHANNEL, BIN_CHANNEL
        print("🔄 Force-linking channels...")
        
        # We try multiple ways to force Telegram to recognize these IDs
        for channel_id in [LOG_CHANNEL, BIN_CHANNEL]:
            try:
                # Force a chat fetch
                chat = await self.get_chat(channel_id)
                # Force a message fetch to 'warm up' the peer
                async for _ in self.get_chat_history(channel_id, limit=1):
                    break
                print(f"✅ Peer Link Verified: {chat.title}")
            except Exception as e:
                print(f"⚠️ Peer Warm-up Failed for {channel_id}: {e}")

        # --- REST OF YOUR WEB SERVER CODE ---
        # (Keep your aiohttp setup here exactly as it was)
        
