from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI

class Database:
    def __init__(self):
        # Connects to your MongoDB using the URI in Koyeb
        self.client = AsyncIOMotorClient(DATABASE_URI)
        self.db = self.client["FileToLinkBot"]
        self.users = self.db["users"]

    async def add_user(self, user_id):
        user = {"_id": user_id}
        try:
            await self.users.insert_one(user)
        except:
            pass # User already exists in DB

    async def get_all_users(self):
        return self.users.find({})

    async def total_users_count(self):
        return await self.users.count_documents({})

# This is the "db" object start.py is looking for
db = Database()
