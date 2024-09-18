from crud.tags import TagService
from database.db import engine, Base, async_session


# Создание таблиц в БД при запуске приложения
async def init_models() -> None:
    async with engine.begin() as conn:
        # Создание таблиц в БД
        await conn.run_sync(Base.metadata.create_all)


# Создание записей в БД при запуске приложения
async def create_tags():
    async with async_session() as session:
        tag_service = TagService(session)
        try:
            await tag_service.create_tag('DAILY')
            await tag_service.create_tag('IMPORTANT')
            await tag_service.create_tag('WEEKLY')
        except Exception:
            pass
        finally:
            await session.close()
