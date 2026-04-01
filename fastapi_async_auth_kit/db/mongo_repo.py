from motor.motor_asyncio import AsyncIOMotorClient

class MongoRepo:
    def __init__(self, url):
        client = AsyncIOMotorClient(url)
        db = client["auth"]
        self.users = db["users"]
        self.tokens = db["tokens"]

    async def get_user(self, username):
        return await self.users.find_one({"username": username})

    async def create_user(self, u, p):
        await self.users.insert_one({"username": u, "password": p})

    async def save_refresh_token(self, token):
        await self.tokens.insert_one({"token": token, "blacklisted": False})

    async def is_token_blacklisted(self, token):
        t = await self.tokens.find_one({"token": token})
        return t and t["blacklisted"]

    async def blacklist_token(self, token):
        await self.tokens.update_one(
            {"token": token},
            {"$set": {"blacklisted": True}}
        )