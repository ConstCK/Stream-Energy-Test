import logging

from fastapi import FastAPI, Request
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
# Логирование
logger = logging.getLogger("my_fastapi_app")
logging.basicConfig(
    filename='../logs.txt',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


# Включение маршрутов в основное приложение
app.include_router(user_router, tags=['users'])
app.include_router(note_router, tags=['notes'])
app.include_router(tag_router, tags=['tags'])


@app.get('/', description='Приветственная надпись', )
async def greetings() -> dict:
    return {'message': 'Greetings, sir'}


# Запуск сервера
if __name__ == '__main__':
    # For development only (too slow for production)

    uvicorn.run('main:app', host=settings.host, port=8000, reload=True)
