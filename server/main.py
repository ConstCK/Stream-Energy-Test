from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import uvicorn

from config import settings

from initial_tasks import init_models, create_tags

from routers.users import router as user_router
from routers.notes import router as note_router
from routers.tags import router as tag_router


# Создание события при запуске (и остановке) сервера (если нужно)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('startup')
    await init_models()
    await create_tags()

    yield
    print('shutdown')


# Создание основного приложения
app = FastAPI(
    title='My notes',
    description='For StreamEnergy test...',
    lifespan=lifespan
)

# Включение маршрутов в основное приложение
app.include_router(user_router, tags=['users'])
app.include_router(note_router, tags=['notes'])
app.include_router(tag_router, tags=['tags'])


@app.get('/', description='Приветственная надпись', )
async def greetings() -> dict:
    return {'message': 'Greetings, sir'}


# Запуск сервера
if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.host, port=8000, reload=True)
