from fastapi import HTTPException, status, Response, Request
from passlib.context import CryptContext
from jose import jwt, JWTError

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хеширование чистого пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Проверка соответствия чистого пароля хеш-паролю
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создания токена для авторизированного пользователя
def create_access_token(data: dict[str, int]) -> str:
    to_encode = {'id': data['id']}
    encode_jwt = jwt.encode(claims=to_encode,
                            key=settings.secret_key,
                            algorithm=settings.algorithm)
    return encode_jwt


# Валидация токена
def validate_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token=token, key=settings.secret_key, algorithms=settings.algorithm)
        return payload.get('id')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')


# Получение token из cookies
def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token не найден')
    return token


# Получение токена из cookies и его проверка
def access_granted(request: Request) -> bool:
    token = get_token(request)
    result = validate_access_token(token)
    return True if result else False
