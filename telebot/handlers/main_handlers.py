import datetime
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.keyboards import data_keyboard, tags_keyboard
from crud.notes import create_note, get_all_notes, get_notes_by_tag
from states.states import Stages
from services.utils import valid_text

router = Router()

# Обработчик получения всех заметок


@router.callback_query(F.data == 'all_tasks')
async def cmd_get_tasks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'access_token' in data:
        result = get_all_notes(
            token=data['access_token'], tg_id=callback.from_user.id)

        if len(result) > 0:
            for n, note in enumerate(result):
                date = datetime.datetime.strptime(
                    note['updated_at'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
                await callback.message.answer(text=f'Заметка №{n+1}: Заголовок: {note['title']}\n{note['content']} от {date}\nТеги: {[obj['name'] for obj in note['tags']]}')
            await callback.message.answer(text=f'Получено заметок: {len(result)}', reply_markup=await data_keyboard())
        else:
            await callback.message.answer(text='У Вас нет заметок')
        await callback.answer(text='Получение всех заметок...')
    else:
        await callback.message.answer(text='Авторизуйтесь для продолжения...')

# Обработчик цепочки добавления заметок


@router.callback_query(F.data == 'add_task')
async def cmd_add_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите заголовок для заметки')
    await callback.answer(text='Добавление заголовка для заметки...')
    await state.set_state(Stages.adding_title)

# Обработчик добавления заголовка заметок


@router.message(StateFilter(Stages.adding_title))
async def cmd_add_task_title(message: Message, state: FSMContext):
    if valid_text(message.text):
        await message.answer(text='Введите содержимое заметки')
        await state.set_state(Stages.adding_content)
        await state.update_data(title=message.text)
    else:
        await message.answer(text='Введите заголовок для заметки заново...')

# Обработчик добавления данных заметок


@router.message(StateFilter(Stages.adding_content))
async def cmd_add_task_content(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'access_token' in data:
        token = data['access_token']
        if valid_text(message.text):
            await message.answer(text='Введите тэг для заметки', reply_markup=await tags_keyboard(token, mode='creation'))
            await state.set_state(Stages.adding_tags)
            await state.update_data(content=message.text)
        else:
            await message.answer(text='Введите содержимое для заметки заново...')
    else:
        await message.answer(text='Авторизуйтесь для продолжения...')

# Обработчик отправки заметки на сервер


@router.callback_query(StateFilter(Stages.adding_tags), F.data == 'finish')
async def cmd_complete_task_creation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'tags' not in data:
        await state.update_data(tags=[])
        data = await state.get_data()
    payload = {
        'title': data['title'],
        'content': data['content'],
        'tg_id': callback.from_user.id,
        'tags': data['tags']
    }
    create_note(token=data['access_token'], data=payload)

    await state.set_state(Stages.authed)
    await state.set_data({'access_token': data['access_token']})
    await callback.message.answer(text='Заметка создана', reply_markup=await data_keyboard())
    await callback.answer(text='Создание заметки...')

# Обработчик добавления тэгов для заметки


@router.callback_query(StateFilter(Stages.adding_tags))
async def cmd_add_task_tag(callback: CallbackQuery, state: FSMContext):
    if valid_text(callback.data):
        data = await state.get_data()

        if 'tags' not in data:
            await state.update_data(tags=[callback.data])
        else:
            tags = data['tags']
            tags.append(callback.data)
            await state.update_data(tags=tags)

        await callback.message.answer(text='Можете ввести еще тэг или завершить создание заметки')
        await callback.answer(text='Cоздание тегов для заметки...')
    else:
        await callback.message.answer(text='Введите тэг заново...')


# Обработчик цепочки получения заметок по тегам


@router.callback_query(F.data == 'tasks_by_tags')
async def cmd_add_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'access_token' in data:
        token = data['access_token']
        await callback.message.answer(text='Выберите тег для получения заметок',
                                      reply_markup=await tags_keyboard(token=token, mode='selecting'))
        await callback.answer(text='Получение тегов для заметок...')
        await state.set_state(Stages.selecting_tags)
    else:
        await callback.message.answer(text='Авторизуйтесь для продолжения...')

# Обработчик получения заметок по указанному тегу


@router.callback_query(StateFilter(Stages.selecting_tags))
async def cmd_add_task(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'access_token' in data:

        result = get_notes_by_tag(
            token=data['access_token'], tg_id=callback.from_user.id, tag_id=callback.data)

        if len(result) > 0:
            for n, note in enumerate(result):
                date = datetime.datetime.strptime(
                    note['updated_at'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
                await callback.message.answer(text=f'Заметка №{n+1} с тегом {note['tags'][0]['name']}: Заголовок: {note['title']}\n{note['content']} от {date}')
            await callback.message.answer(text=f'Получено заметок: {len(result)}', reply_markup=await data_keyboard())
        else:
            await callback.message.answer(text='У Вас нет заметок')
        await callback.answer(text='Получение всех заметок...')
    else:
        await callback.message.answer(text='Авторизуйтесь для продолжения...')
