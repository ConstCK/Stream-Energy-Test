from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()



@dp.message(F.text=='Регистрация')
async def cmd_registration(message: Message, state: FSMContext):
    await message.answer(text=f'Welcome to chat {message.from_user.full_name}',
                         reply_markup=await auth_keyboard())

