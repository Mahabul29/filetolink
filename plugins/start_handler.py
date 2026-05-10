from pyrogram import Client, filters
from config import BIN_CHANNEL

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            file_id = int(message.command[1].split("_")[1])
            # Use copy_message for a faster, direct transfer from your storage
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=BIN_CHANNEL,
                message_id=file_id
            )
        except Exception as e:
            print(f"Start Error: {e}")
            await message.reply_text("❌ Error: Could not retrieve the file.")
    else:
        await message.reply_text("👋 Send me a file to generate links!")
        
