from fastapi_auth.db.sqlalchemy_repo import SQLRepo
from fastapi_auth.db.mongo_repo import MongoRepo

async def get_repo(config):
    if config.db_type == "mongodb":
        return MongoRepo(config.db_url)

    repo = SQLRepo(config.db_url)
    await repo.init()
    return repo