from fastapi_async_auth_kit.db.sqlalchemy_repo import SQLRepo
from fastapi_async_auth_kit.db.mongo_repo import MongoRepo

async def get_repo(config):
    if config.db_type == "mongodb":
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(config.db_url)
        db_name = config.db_url.split("/")[-1]
        db = client[db_name]
        repo = MongoRepo(db)
        return repo

    repo = SQLRepo(config.db_url)
    await repo.init()
    return repo