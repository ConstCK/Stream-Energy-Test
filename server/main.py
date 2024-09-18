import logging

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from config import settings

from initial_tasks import init_models, create_tags

from routers.users import router as user_router
from routers.notes import router as note_router
from routers.tags import router as tag_router


# Создание события при запуске (и остановке) сервера (если нужно)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('starting up...')
    await init_models()
    await create_tags()
    yield
    print('shutting down...')


# Создание основного приложения
app = FastAPI(
    title='My notes',
    description='For StreamEnergy test...',
    lifespan=lifespan
)
# Логирование
logger = logging.getLogger("my_fastapi_app")

# Не для продакшн!!!
logging.basicConfig(
    filename='../logs.txt',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)


# Middleware для логирования
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


# Создание ограничителя приложения
limiter = Limiter(key_func=get_remote_address, default_limits=["1000 per day", "100 per hour"])

# Включение маршрутов в основное приложение
app.include_router(user_router, tags=['users'])
app.include_router(note_router, tags=['notes'])
app.include_router(tag_router, tags=['tags'])

# Добавление ограничителя скорости в основное приложение
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


# Приветственный маршрут
@app.get('/', description='Приветственная надпись', )
async def greetings() -> dict:
    return {'message': 'Greetings, sir'}


# Запуск сервера
if __name__ == '__main__':
    # For development only (too slow for production)

    uvicorn.run('main:app', host=settings.host, port=8000, reload=True)
