from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from services.constants import AUTH_COMMANDS, MAIN_COMMANDS
from crud.tags import get_all_tags


# Создание клавиатуры для auth
async def auth_keyboard():
    builder = ReplyKeyboardBuilder()
    for c in AUTH_COMMANDS:
        builder.add(KeyboardButton(text=c))
    return builder.adjust(2).as_markup(resize_keyboard=True)

# Создание клавиатуры для получения данных


async def data_keyboard():
    builder = InlineKeyboardBuilder()
    for k, v in MAIN_COMMANDS.items():
        builder.add(InlineKeyboardButton(text=v, callback_data=k))
    return builder.adjust(2).as_markup()

# Создание клавиатуры для получения всех тегов


async def tags_keyboard(token: str, mode: str):
    data = get_all_tags(token)
    builder = InlineKeyboardBuilder()
    for tag in data:
        builder.add(InlineKeyboardButton(
            text=tag['name'], callback_data=str(tag['id'])))
    if mode == 'creation':
        builder.add(InlineKeyboardButton(
            text='Отправить данные', callback_data='finish'))

    return builder.adjust(2).as_markup()
