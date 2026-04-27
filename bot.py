from utils.channel import resolve_bin_channel

async def main():
    async with app:
        me = await app.get_me()
        logger.info(f"✅ Bot Started as @{me.username}")

        # ✅ Use the new resolver
        resolved = await resolve_bin_channel(app)
        if not resolved:
            logger.error("❌ BIN_CHANNEL could not be resolved. Files may not save correctly.")

        runner = await web_server()
        logger.info(f"🌐 Web server started")

        try:
            await asyncio.Event().wait()
        finally:
            await runner.cleanup()
            logger.info("🛑 Web server stopped cleanly")
