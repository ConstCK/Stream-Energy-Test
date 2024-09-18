import asyncio
import logging

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher

from config import settings
from keyboards.keyboards import auth_keyboard
from handlers.auth_handlers import router as auth_router
from handlers.main_handlers import router as main_router

# Создание бота
bot = Bot(token=settings.bot_token.get_secret_value())

# Создание диспетчера для обработки событий
dp = Dispatcher()

# Добавление маршрута с обработчиками к диспетчеру
dp.include_routers(auth_router, main_router)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f'Welcome to chat {message.from_user.full_name}. Вам нужно авторизоваться для получения данных.',
                         reply_markup=await auth_keyboard())


async def main():
    # Удаление всех необработанных сообщений после отключения бота
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск обработчика всех событий
    await dp.start_polling(bot)


if __name__ == '__main__':
    # For development only (too slow for production)

    logging.basicConfig(
        filename='../logs.txt',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exiting program...')
