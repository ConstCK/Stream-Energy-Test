from fastapi import APIRouter, status, Depends

from crud.users import UserService
from schemas.users import UserCreation

# Маршрут для auth
router = APIRouter(prefix='/api/v1/users')


# Маршрут для регистрации нового пользователя
@router.post('/signup', description='Registration',
             status_code=status.HTTP_201_CREATED, name='user_registration',
             responses={201: {'description': 'Успешная регистрация'},
                        409: {'description': 'Пользователь уже существует'}}
             )
async def signup(data: UserCreation, service: UserService = Depends()) -> dict[str, str]:
    result = await service.create_user(data)

    return result


# Маршрут для авторизации пользователя
@router.post('/login', description='Authorization',
             status_code=status.HTTP_201_CREATED, name='user_authorization',
             responses={201: {'description': 'Успешная авторизация'},
                        404: {'description': 'Пользователь не существует'}}
             )
async def login(data: UserCreation, service: UserService = Depends()) -> dict[str, str]:
    result = await service.login_user(data)

    return result
