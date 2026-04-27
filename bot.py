import asyncio
from aiohttp import web
# ... your existing imports ...

async def main():
    # Start Telegram client
    await client.start()
    print("✅ Bot is now running...")   # This will show in Koyeb logs
    
    # Simple web server for Koyeb health check
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is running!"))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    
    print(f"🌐 Web server running on port {os.getenv('PORT', 8080)}")
    
    await asyncio.Event().wait()   # Keep running forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
