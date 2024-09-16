from fastapi import APIRouter, status, Depends, Response

from crud.users import UserService
from schemas.users import User, UserCreation
from services.auth import delete_token, set_token, access_granted

# Маршрут с добавлением функции-проверки прав доступа check_access
router = APIRouter(prefix='/api/v1/users')


# Маршрут для получения всех user для авторизированных пользователей (при наличии token в cookies)
@router.get('/', description='Some description', response_model=list[User],
            status_code=status.HTTP_200_OK, name='get_all_users_url',
            responses={200: {'description': 'Успешное получение объектов'}, }
            )
async def get_all_users(service: UserService = Depends(), permission: bool = Depends(access_granted)):
    if permission:
        result = await service.get_users()
        return result


# Маршрут для регистрации нового пользователя (с использованием cookies)
@router.post('/signup', description='Registration',
             status_code=status.HTTP_201_CREATED, name='user_registration',
             responses={201: {'description': 'Успешная регистрация'},
                        409: {'description': 'Пользователь уже существует'}}
             )
async def signup(response: Response, data: UserCreation, service: UserService = Depends()) -> dict[str, str]:
    result = await service.create_user(data)
    set_token(response, result['token'])
    return result


# Выход из системы с использованием cookies
@router.get('/logout', description='Logout',
            status_code=status.HTTP_200_OK, name='user_logout',
            responses={200: {'description': 'Успешный выход из системы'},
                       }
            )
async def logout(response: Response) -> dict['str', 'str']:
    # Logout из системы
    delete_token(response)
    return {'message': 'Пользователь успешно вышел из системы'}


