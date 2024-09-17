from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Базовая схема для user
class BaseUser(BaseModel):
    username: str = Field(min_length=2, max_length=24,
                          description='Имя пользователя')
    tg_id: int


# Схема для получения user
class User(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Схема для создания user
class UserCreation(BaseUser):
    password: str = Field(description='Пароль пользователя',
                          min_length=4,
                          max_length=16)



