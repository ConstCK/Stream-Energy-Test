from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tags import TagService
from database.db import get_db
from models.models import User as UserTable
from schemas.users import User, UserCreation
from services.auth import get_password_hash, create_access_token, validate_access_token


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_db),
                 tag_service: TagService = Depends()) -> None:
        self.db = session
        self.tag_service = tag_service

    # Получение списка всех пользователей
    async def get_users(self, tg_id: int) -> list[User] | list:
        query = select(UserTable).where(UserTable.tg_id == tg_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    # Получение пользователя по имени
    async def get_user_by_tg_id(self, tg_id: int) -> User:
        query = select(UserTable).where(UserTable.tg_id == tg_id)
        result = await self.db.execute(query)
        return result.scalar()

    # Создание пользователя(регистрация)
    async def create_user(self, data: UserCreation) -> dict['str', 'str']:
        query = select(UserTable).where(UserTable.tg_id == data.tg_id)
        db_user = await self.db.execute(query)
        result = db_user.scalar()

        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')

        hashed_password = get_password_hash(data.password)
        db_user = UserTable(username=data.username,
                            password=hashed_password,
                            tg_id=data.tg_id)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        query = select(UserTable).where(UserTable.tg_id == data.tg_id)
        db_user = await self.db.execute(query)
        user = db_user.scalar()
        token = create_access_token({'id': user.tg_id})
        return {'message': 'Регистрация прошла успешно',
                'user': user.username, 'token': token}

    # Проверка доступа к данным
    async def access_granted(self, token: str) -> bool:
        tg_id = validate_access_token(token)
        query = select(UserTable).where(UserTable.tg_id == tg_id)
        result = await self.db.execute(query)
        return True if result else False
