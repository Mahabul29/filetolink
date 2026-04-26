from database.users_db import db

async def ban_user(user_id, reason):
    await db.col.update_one(
        {'id': user_id},
        {'$set': {'banned': True, 'reason': reason}},
        upsert=True
    )

async def unban_user(user_id):
    await db.col.update_one(
        {'id': user_id},
        {'$set': {'banned': False}}
    )

async def is_user_banned(user_id):
    user = await db.col.find_one({'id': user_id})
    return user.get('banned', False) if user else False
  
