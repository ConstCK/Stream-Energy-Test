from fastapi import APIRouter, status, Depends, Response

from crud.users import UserService
from schemas.users import User, UserCreation


# Маршрут с добавлением функции-проверки прав доступа check_access
router = APIRouter(prefix='/api/v1/users')


# Маршрут для регистрации нового пользователя (с использованием cookies)
@router.post('/', description='Registration',
             status_code=status.HTTP_201_CREATED, name='user_registration',
             responses={201: {'description': 'Успешная регистрация'},
                        409: {'description': 'Пользователь уже существует'}}
             )
async def signup(data: UserCreation, service: UserService = Depends()) -> dict[str, str]:
    result = await service.create_user(data)

    return result




