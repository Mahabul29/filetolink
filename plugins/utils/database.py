from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self.client["FileToLinkBot"]
        self.users = self.db["users"]

    async def add_user(self, user_id):
        try:
            await self.users.insert_one({"_id": user_id})
        except:
            pass 

    async def get_all_users(self):
        return self.users.find({})

    async def total_users_count(self):
        return await self.users.count_documents({})

db = Database()
