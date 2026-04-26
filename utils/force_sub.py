from pyrogram.errors import UserNotParticipant
from info import Var
from Script import script

async def is_subscribed(bot, message):
    if not Var.UPDATES_CHANNEL:
        return True
    try:
        user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.from_user.id)
        if user.status == "kicked":
            return False
    except UserNotParticipant:
        return False
    except Exception:
        return True
    return True
  
