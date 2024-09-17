import json
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from crud.auth import login_user, register_user
from states.states import Stages
from services.utils import valid_password
from keyboards.keyboards import auth_keyboard

router = Router()


@router.message(F.text == 'Регистрация')
async def cmd_registration(message: Message, state: FSMContext):
    await message.answer(text=f'Укажите пароль {message.from_user.full_name}...', )
    await state.set_state(Stages.password_verifying)


@router.message(StateFilter(Stages.password_verifying))
async def cmd_registration(message: Message, state: FSMContext):
    data = {
        'name': message.from_user.full_name,
        'password': message.text,
        'tg_id': message.from_user.id
    }
    if not valid_password(message.text):
        await message.answer(text='Неподходящий пароль. Повторите ввод пароля пожалуйста')
    try:
        result = register_user(data)
        data = json.loads(result)

        await state.set_state(state=Stages.authenticated)
        await state.update_data(token=data['token'])
        await message.answer(text=f'Регистрация прошла успешно.Ваш токен для авторизации {data['token']}')
    except Exception:
        await message.answer(text='Произошла ошибка регистрации...',
                             reply_markup=await auth_keyboard())


@router.message(StateFilter(Stages.authenticated), F.text == 'Выход')
async def cmd_logout(message: Message, state: FSMContext):
    state.clear()

    await message.answer(text='Вы вышли из аккаунта. Для получения данных авторизируйтесь снова.')


@router.message(F.text == 'Авторизация')
async def cmd_registration(message: Message, state: FSMContext):
    await message.answer(text=f'Укажите пароль {message.from_user.full_name}...', )
    await state.set_state(Stages.authorization)


@router.message(StateFilter(Stages.authorization))
async def login_handler(message: Message, state: FSMContext):
    data = {
        'name': message.from_user.full_name,
        'password': message.text,
        'tg_id': message.from_user.id
    }
    if not valid_password(message.text):
        await message.answer(text='Неподходящий пароль. Повторите ввод пароля пожалуйста...')

    try:
        result = login_user(data)
        data = json.loads(result)
        print('111')

        await state.set_state(state=Stages.authenticated)
        print('222')
        print(type(data))
        print(data)
        await state.update_data(token=data['token'])
        print('333')
        await message.answer(text=f'Вы успешно авторизировались. Ваш токен для авторизации {data['token']}')
    except Exception:
        await message.answer(text='Произошла ошибка авторизации...',
                             reply_markup=await auth_keyboard())
