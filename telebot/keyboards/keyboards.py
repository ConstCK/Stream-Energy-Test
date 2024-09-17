from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from services.constants import AUTH_COMMANDS


# Создание клавиатуры для использования в /start
async def auth_keyboard():
    builder = ReplyKeyboardBuilder()
    for c in AUTH_COMMANDS:
        builder.add(KeyboardButton(text=c))
    return builder.adjust(2).as_markup(resize_keyboard=True)
