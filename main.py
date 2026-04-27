
# ── Entry point ───────────────────────────────────────────────────────────────
async def main():
    async with app:
        me = await app.get_me()
        logger.info(f"✅ Bot Started as @{me.username}")

        # Start the web server FIRST (Highest Priority for Koyeb Health Checks)
        runner = await web_server()
        logger.info(f"✅ Web server started successfully on port 8080")

        # Try to resolve the channel, but don't let an error stop the bot
        try:
            await resolve_bin_channel(app)
        except Exception as e:
            logger.warning(f"⚠️ Startup channel check skipped: {e}")

        logger.info("🚀 Bot is now fully online and waiting for files.")

        try:
            await asyncio.Event().wait()   # Keep running forever
        finally:
            await runner.cleanup()
            logger.info("🛑 Web server stopped cleanly")
            
