import datetime
import enum

from sqlalchemy import String, func, ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


# Класс для использования предопределенных значений
class TagName(enum.Enum):
    DAILY = 'ежедневные'
    WEEKLY = 'еженедельные'
    IMPORTANT = 'важные'


# Связующая таблица (Many-To-Many принцип) для Notes и Tags
class NoteTag(Base):
    __tablename__ = 'notes_tags_association'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    note_id: Mapped[int] = mapped_column(ForeignKey('notes.id', ondelete='SET NULL'))
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id', ondelete='SET NULL'))

    __table_args__ = (UniqueConstraint('note_id', 'tag_id'),)


# Таблица с пользователями
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    username: Mapped[str]
    password: Mapped[str]
    notes: Mapped[list['Note']] = relationship(back_populates='user')


# Таблица с заметками
class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(64))
    content: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),
                                                          server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=func.now(),
                                                          server_default=func.now(),
                                                          onupdate=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='notes')
    tags: Mapped[list['Tag']] = relationship(secondary='notes_tags_association',
                                             back_populates='notes',
                                             )


# таблица с тегами
class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[TagName] = mapped_column(unique=True)
    notes: Mapped[list['Note']] = relationship(secondary='notes_tags_association',
                                               back_populates='tags'
                                               )
