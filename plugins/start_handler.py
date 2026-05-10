from pyrogram import Client, filters
from config import BIN_CHANNEL

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    # This checks if the link clicked was like /start file_865
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        try:
            # 1. Extract the message ID from the command
            file_id = int(message.command[1].split("_")[1])
            
            # 2. Get that exact message from your Storage Channel
            msg = await client.get_messages(BIN_CHANNEL, file_id)
            
            if msg and msg.media:
                # 3. Use 'copy' to send the EXACT same file to the user
                await msg.copy(chat_id=message.chat.id)
            else:
                await message.reply_text("❌ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ꜱᴛᴏʀᴀɢᴇ.")
                
        except Exception as e:
            print(f"Start Handler Error: {e}")
            await message.reply_text("❌ ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ʀᴇᴛʀɪᴇᴠᴇ ꜰɪʟᴇ.")
    else:
        # Standard welcome message for users who just send /start
        await message.reply_text("👋 ꜱᴇɴᴅ ᴍᴇ ᴀ ꜰɪʟᴇ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʟɪɴᴋꜱ!")
      
