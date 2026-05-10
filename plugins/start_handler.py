from pyrogram import Client, filters
from config import BIN_CHANNEL

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].split("_")[1])
            
            # Use 'copy' which is faster and keeps the peer connection alive
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=BIN_CHANNEL,
                message_id=file_id
            )
        except Exception as e:
            # If it fails, try one more time by fetching the message first
            try:
                msg = await client.get_messages(BIN_CHANNEL, file_id)
                await msg.copy(message.chat.id)
            except:
                await message.reply_text("❌ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ. ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍᴏᴍᴇɴᴛ.")
    else:
        await message.reply_text("👋 Welcome! Send me a file to get started.")
        
