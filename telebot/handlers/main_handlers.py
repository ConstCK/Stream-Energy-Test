from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.callback_query(CommandStart())
async def initial_cmd(message: Message):
    await message.answer(text='Добро пожаловать в приложение "Мои заметки"',
                         )
