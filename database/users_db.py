import motor.motor_asyncio
from info import Var

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    async def add_user(self, id):
        user = dict(id=id)
        if not await self.col.find_one({'id': id}):
            await self.col.insert_one(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

db = Database(Var.DATABASE_URL, Var.name)
