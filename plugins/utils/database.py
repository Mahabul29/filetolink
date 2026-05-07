from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self.client["FileToLinkBot"]
        self.users = self.db["users"]

    async def add_user(self, user_id):
        # Using update_one with upsert=True is cleaner than try/except
        # because it won't throw an error if the user already exists.
        await self.users.update_one(
            {"_id": user_id},
            {"$set": {"_id": user_id}},
            upsert=True
        )

    async def get_all_users(self):
        # This returns a cursor that you can use in an 'async for' loop
        return self.users.find({})

    async def total_users_count(self):
        return await self.users.count_documents({})

db = Database()
