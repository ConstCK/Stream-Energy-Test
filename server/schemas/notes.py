# Базовая схема для user
import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict

from schemas.tags import Tag


class BaseNote(BaseModel):
    title: str = Field(max_length=64, description='Заголовок заметки')
    content: str = Field(description='Текст заметки')


class Note(BaseNote):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: int
    tags: list[Tag]

    model_config = ConfigDict(from_attributes=True)


class NoteCreation(BaseNote):
    tg_id: int
    tags: list[str]


class NoteUpdate(BaseNote):
    tags: list[str]
