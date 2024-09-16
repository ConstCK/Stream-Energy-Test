from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db


class NoteService:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.db = session

