from info import Var

async def log_user(bot, user):
    if Var.NEW_USER_LOG:
        await bot.send_message(
            Var.NEW_USER_LOG,
            f"👤 <b>New User Joined!</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"📛 <b>Name:</b> {user.mention}\n"
            f"🔗 <b>Username:</b> @{user.username if user.username else 'None'}"
        )
      
