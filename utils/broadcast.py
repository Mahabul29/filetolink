import asyncio
from database.users_db import db
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

async def send_broadcast(bot, admin_id, message):
    all_users = await db.get_all_users()
    success = 0
    failed = 0
    
    msg = await bot.send_message(admin_id, "<code>Broadcasting started...</code>")
    
    async for user in all_users:
        try:
            await message.copy(chat_id=user['id'])
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.copy(chat_id=user['id'])
            success += 1
        except (UserIsBlocked, InputUserDeactivated):
            failed += 1
        except Exception:
            failed += 1
            
    await msg.edit(f"<b>Broadcast Completed!</b>\n\n✅ Success: {success}\n❌ Failed: {failed}")
  
