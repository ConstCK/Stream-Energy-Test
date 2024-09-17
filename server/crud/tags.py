from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from schemas.tags import Tag
from models.models import Tag as TagTable


class TagService:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.db = session

    async def get_tag_by_name(self, name: str) -> Tag:
        query = select(TagTable).where(TagTable.name == name)
        result = await self.db.execute(query)
        return result.scalar()

    async def create_tag(self, name: str) -> Tag:
        query = insert(TagTable).values({'name': name}).returning(TagTable)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar()



