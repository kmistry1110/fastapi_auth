from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, select
from fastapi_async_auth_kit.schemas.user import UserModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))

class Token(Base):
    __tablename__ = "tokens"
    token = Column(String(512), primary_key=True)
    blacklisted = Column(Integer, default=0)


class SQLRepo:
    def __init__(self, url):
        self.engine = create_async_engine(url, future=True)
        self.Session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_user(self, username):
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        return UserModel(
            id=str(user.id),
            username=user.username,
            password=user.password
        )

    async def create_user(self, u, p):
        async with self.Session() as db:
            user = User(username=u, password=p)
            db.add(user)
            await db.commit()
            return user

    async def save_refresh_token(self, token):
        async with self.Session() as db:
            db.add(Token(token=token))
            await db.commit()

    async def is_token_blacklisted(self, token):
        async with self.Session() as db:
            res = await db.execute(select(Token).where(Token.token == token))
            t = res.scalar_one_or_none()
            return t and t.blacklisted == 1

    async def blacklist_token(self, token):
        async with self.Session() as db:
            res = await db.execute(select(Token).where(Token.token == token))
            t = res.scalar_one_or_none()
            if t:
                t.blacklisted = 1
                await db.commit()