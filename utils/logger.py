from config import LOG_CHANNEL

async def log_user(bot, user):
    if LOG_CHANNEL:
        await bot.send_message(
            LOG_CHANNEL,
            f"👤 <b>New User Joined!</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"📛 <b>Name:</b> {user.mention}\n"
            f"🔗 <b>Username:</b> @{user.username if user.username else 'None'}"
        )
