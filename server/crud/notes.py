from fastapi import Depends
from sqlalchemy import select, insert, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.users import UserService
from crud.tags import TagService
from database.db import get_db
from schemas.notes import NoteCreation, NoteUpdate, Note
from models.models import Note as NoteTable
from models.models import Tag as TagTable


class NoteService:
    def __init__(self, session: AsyncSession = Depends(get_db),
                 user_service: UserService = Depends(),
                 tag_service: TagService = Depends()) -> None:
        self.db = session
        self.user_service = user_service
        self.tag_service = tag_service

    # Получение всех заметок или заметок с тегами (если они указанны)
    async def get_all_notes(self, tg_id: int, tag_id: int = None) -> list[Note] | list:
        user = await self.user_service.get_user_by_tg_id(tg_id)
        if tag_id:
            tag_object = await self.tag_service.get_tag_by_id(tag_id)
            if tag_object is not None:
                query = (select(NoteTable)
                         .where(NoteTable.user_id == user.id)
                         .where(NoteTable.tags.any(TagTable.id == tag_object.id))
                         .options(selectinload(NoteTable.tags)))
            else:
                return []
        else:
            query = (select(NoteTable)
                     .where(NoteTable.user_id == user.id)
                     .options(selectinload(NoteTable.tags)))
        result = await self.db.execute(query)

        return result.scalars().all()

    # Получение заметки по id
    async def get_note_by_id(self, note_id: int, tg_id: int):
        user = await self.user_service.get_user_by_tg_id(tg_id)

        query = (select(NoteTable)
                 .where(and_(NoteTable.id == note_id, NoteTable.user_id == user.id))
                 .options(selectinload(NoteTable.tags)))
        result = await self.db.execute(query)

        return result.scalar()

    # Создание заметки
    async def create_note(self, data: NoteCreation) -> dict:
        user = await self.user_service.get_user_by_tg_id(data.tg_id)
        query = insert(NoteTable).values({
            'title': data.title,
            'content': data.content,
            'user_id': user.id,
        }).returning(NoteTable).options(selectinload(NoteTable.tags))
        result = await self.db.scalar(query)

        for i in data.tags:
            tag = await self.tag_service.get_tag_by_id(tag_id=int(i))
            result.tags.append(tag)

        await self.db.commit()
        await self.db.refresh(result)
        return {'message': 'Создание заметки прошло успешно',
                'note': result.title, 'content': result.content}

    # Удаление заметки
    async def delete_note(self, note_id: int) -> dict[str, str]:
        try:
            note = await self.db.get(NoteTable, note_id)
            await self.db.delete(note)
            await self.db.commit()
            return {'message': f'Заметка № {note_id} успешно удалена'}

        except Exception as err:
            return {'message': f'Удаление заметки не удалось -> {err}'}

    # Обновление заметки
    async def update_note(self, note_id: int, data: NoteUpdate) -> dict[str, str]:
        try:
            query = (update(NoteTable).where(NoteTable.id == note_id).values(
                {'title': data.title, 'content': data.content})
                     .returning(NoteTable)
                     .options(selectinload(NoteTable.tags)))
            result = await self.db.execute(query)
            result = result.scalar()
            result.tags = []
            for i in data.tags:
                tag = await self.tag_service.get_tag_by_name(name=i)
                result.tags.append(tag)

            await self.db.commit()
            await self.db.refresh(result)
            return {'message': f'Заметка № {note_id} успешно обновлена'}
        except Exception as err:
            return {'message': f'Обновление заметки не удалось -> {err}'}
