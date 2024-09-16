from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Базовая схема для user
class BaseUser(BaseModel):
    username: str = Field(min_length=2, max_length=24,
                          description='Имя пользователя')
    email: EmailStr = Field(description='Адрес электронной почты пользователя')


# Схема для получения user
class User(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Схема для создания user
class UserCreation(BaseUser):
    password: str = Field(description='Пароль пользователя',
                          min_length=4,
                          max_length=16)


# Схема для ввода данных user для авторизации
class AuthUser(BaseModel):
    email: EmailStr = Field(description='Адрес электронной почты пользователя')
    password: str = Field(description='Пароль пользователя',
                          min_length=4,
                          max_length=16)
