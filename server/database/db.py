from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.db_url, echo=True)

async_session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Создание класса-родителя для наследования при создании моделей
class Base(DeclarativeBase):
    pass


# Создание сессии
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_models() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # Создание таблиц в БД
        await conn.run_sync(Base.metadata.create_all)
