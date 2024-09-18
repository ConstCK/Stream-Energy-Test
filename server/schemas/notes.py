import datetime
from pydantic import BaseModel, Field, ConfigDict

from schemas.tags import Tag


# Базовая схема для заметки
class BaseNote(BaseModel):
    title: str = Field(max_length=64, description='Заголовок заметки')
    content: str = Field(description='Текст заметки')


# Схема для получения заметки
class Note(BaseNote):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: int
    tags: list[Tag]

    model_config = ConfigDict(from_attributes=True)


# Схема для создания заметки
class NoteCreation(BaseNote):
    tg_id: int
    tags: list[str]


# Схема для обновления заметки
class NoteUpdate(BaseNote):
    tags: list[str]
