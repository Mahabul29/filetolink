import asyncio
from pyrogram import Client
from config import LOG_CHANNEL, BIN_CHANNEL

async def refresh_peers(client: Client):
    """
    Forces the bot to resolve channel IDs on startup 
    to prevent 'Peer id invalid' errors.
    """
    print("🔄 [BOOT] Refreshing Peer IDs...")
    try:
        # Resolve LOG_CHANNEL
        await client.get_chat(LOG_CHANNEL)
        print(f"✅ [BOOT] Connected to Log Channel: {LOG_CHANNEL}")
        
        # Resolve BIN_CHANNEL
        await client.get_chat(BIN_CHANNEL)
        print(f"✅ [BOOT] Connected to Bin Channel: {BIN_CHANNEL}")
        
    except Exception as e:
        print(f"❌ [BOOT] Critical Error during peer refresh: {e}")
        print("💡 Ensure the bot is an ADMIN in both channels and the IDs are correct.")

# This function can be called from your main.py or Bot class
