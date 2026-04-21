from fastapi_async_auth_kit.schemas.user import UserModel


class MongoRepo:
    def __init__(self, db):
        self.collection = db["users"]
        self.token_collection = db["tokens"]

    async def create_user(self, username, password):
        user = {"username": username, "password": password}
        result = await self.collection.insert_one(user)

        user["id"] = str(result.inserted_id)
        return UserModel(**user)

    async def get_user(self, username):
        user = await self.collection.find_one({"username": username})

        if not user:
            return None

        # Convert Mongo _id → id
        user["id"] = str(user["_id"])
        user.pop("_id", None)

        return UserModel(**user)

    async def save_refresh_token(self, token):
        await self.token_collection.insert_one({
            "token": token,
            "blacklisted": False
        })

    async def blacklist_token(self, token):
        await self.token_collection.update_one(
            {"token": token},
            {"$set": {"blacklisted": True}}
        )

    async def is_token_blacklisted(self, token):
        data = await self.token_collection.find_one({"token": token})
        return data and data.get("blacklisted", False)