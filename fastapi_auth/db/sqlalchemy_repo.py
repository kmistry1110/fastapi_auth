from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, select

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

class Token(Base):
    __tablename__ = "tokens"
    token = Column(String, primary_key=True)
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
        async with self.Session() as db:
            res = await db.execute(select(User).where(User.username == username))
            return res.scalar_one_or_none()

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