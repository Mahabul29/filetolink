import motor.motor_asyncio
from info import Var

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    async def add_user(self, id):
        user = {'id': id}
        if not await self.col.find_one({'id': id}):
            await self.col.insert_one(user)

db = Database(Var.DATABASE_URL, Var.name)
