from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from schemas.tags import Tag
from models.models import Tag as TagTable


class TagService:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.db = session

    # Получение тега по имени
    async def get_tag_by_name(self, name: str) -> Tag:
        query = select(TagTable).where(TagTable.name == name)
        result = await self.db.execute(query)
        return result.scalar()

    # Получение тега по id
    async def get_tag_by_id(self, tag_id: int) -> Tag:
        query = select(TagTable).where(TagTable.id == tag_id)
        result = await self.db.execute(query)
        return result.scalar()

    # Создание тегов
    async def create_tag(self, name: str) -> Tag:
        query = insert(TagTable).values({'name': name}).returning(TagTable)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar()

    # Получение всех тегов
    async def get_all_tags(self, ) -> list[Tag]:
        query = select(TagTable)
        result = await self.db.execute(query)
        return result.scalars().all()
