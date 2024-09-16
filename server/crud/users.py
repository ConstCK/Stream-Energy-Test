from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.users import User as UserTable
from schemas.users import User, UserCreation, AuthUser
from services.auth import get_password_hash, create_access_token, verify_password


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        self.db = session

    # Получение списка всех пользователей
    async def get_users(self) -> list[User] | list:
        query = select(UserTable)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    # Создание пользователя(регистрация)
    async def create_user(self, data: UserCreation) -> dict['str', 'str']:
        query = select(UserTable).where(UserTable.email == data.email)
        db_user = await self.db.execute(query)
        result = db_user.scalar()

        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')

        hashed_password = get_password_hash(data.password)
        db_user = UserTable(username=data.username,
                            password=hashed_password,
                            email=data.email)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        query = select(UserTable).where(UserTable.email == data.email)
        db_user = await self.db.execute(query)
        user = db_user.scalar()
        token = create_access_token({'id': user.id})
        return {'message': 'Регистрация прошла успешно',
                'user': user.username, 'token': token}

    # Аутентификация пользователя (проверка email&password)
    async def authenticate_user(self, data: AuthUser) -> User | None:
        query = select(UserTable).where(UserTable.email == data.email)
        db_user = await self.db.execute(query)
        result = db_user.scalar()
        if (not db_user or
                verify_password(plain_password=data.password,
                                hashed_password=result.password) is False):
            return None
        return result






