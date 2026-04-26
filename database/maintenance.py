from database.users_db import db

async def set_maintenance(state: bool):
    await db.db.settings.update_one(
        {'id': 'maintenance'},
        {'$set': {'state': state}},
        upsert=True
    )

async def get_maintenance():
    settings = await db.db.settings.find_one({'id': 'maintenance'})
    return settings.get('state', False) if settings else False
  
