import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    # host: str = 'localhost'
    host: str = '0.0.0.0'

    # Url для postgresql связи
    db_url: str = (f'postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}'
                   f'@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}')

    # Данные для использования токен-авторизации
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')

    # Настройки для использования переменных из .env
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='allow')


settings = Settings()
